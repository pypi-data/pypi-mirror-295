import sys
import os
import subprocess
import requests
import tarfile
import time
from threading import Thread
from datetime import datetime, timezone
import boto3
import json
import re
from positron_common.config import parse_job_config

'''_______________________________________________________________________________________
    
    INITIALIZING CONFIGURATION AND CONSTANTS
    ______________________________________________________________________________________
'''
# Disable stdout buffering
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['POSITRON_CLOUD_ENVIRONMENT'] = '1'

# Define API endpoints
API_BASE = os.environ.get('API_ENDPOINT')
API_GET_JOB = f'{API_BASE}/get-job'
API_UPDATE_JOB = f'{API_BASE}/update-job'
API_JOB_LIFECYCLE = f'{API_BASE}/check-lifecycle'

# Define AWS S3 attached folders
working_dir = "/usr/src/job-execution"
results_dir = "/usr/src/job-controller/ws/result"
aws_region = os.getenv("REGION", "us-west-2")

# Define cross component enums
job_statuses = dict(
    pending="pending",
    uploading="uploading",
    in_queue="in_queue",
    launching="launching_pod",
    pulling_image="pulling_image",
    pulled_image="pulled_image",
    starting_container="starting_container",
    started_container="started_container",
    initializing="initializing",
    computing="computing",
    storing="storing",
    complete="complete",
    failed="failed",
    execution_error="execution_error",
    terminate="terminate_job",
    terminated="terminated"
)
log_types = dict(
    stdout="INFO",
    stderr="ERROR",
    debug="DEBUG"
)

# Cycle intervals
charge_interval = int(os.getenv('POSITRON_CHARGE_INTERVAL', 60))
stdout_log_interval = int(os.getenv('POSITRON_STDOUT_INTERVAL', 2))
check_termination_interval = int(os.getenv('POSITRON_CHECK_TERMINATION_INTERVAL', 10))

# Job management
running_job = None
kill_threads = False
job_id = sys.argv[2]
job = {}
stdout, stderr = [], []
final_status = job_statuses['complete']
return_code = 0

# Request header
headers = {"PositronJobId": job_id,
           "SystemAuthenticationKey": os.environ['SYSTEM_AUTHENTICATION_KEY']}

# Global clients
cloudwatch_client = boto3.client('logs', region_name=aws_region)


'''_______________________________________________________________________________________
    
    SUB MODULES
    ______________________________________________________________________________________
'''
# Get Job -----------------------------------------------------------
def get_job():
    cloud_log('Fetching job details')
    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    global job
    job = resp.json()


# Unpack Workspace  -------------------------------------------------
def unpack_workspace():
    try:
        cloud_log('Unpacking workspace')
        with tarfile.open('ws/workspace.tar.gz') as tar:
            tar.extractall(working_dir)
    except Exception as e:
        cloud_log(e, log_types["debug"])
        cloud_log('Extracting workspace failed', log_types["stderr"])


# Run Job -----------------------------------------------------------
def run_job():
    cloud_log('Starting job')
    update_job(status=job_statuses["computing"])
    
    config_file = os.path.join(working_dir, "job_config.yaml")
    is_generic, commands, env_vars = parse_job_config(config_file)

    if is_generic:
        run_commands(commands, env_vars)
    else:
        run_decorator_job(env_vars)


def run_commands(commands, env_vars):
    cloud_log(f'Found commands to execute:\n{commands}')

    # extract individual commands
    invalid_commands = []
    items = re.split(r'&&|;|\n', commands)
    items = [item.strip() for item in items if item.strip()]

    # validate commands
    for command in items:
        result = subprocess.run(f'command -v {command}', shell=True, capture_output=True)
        if result.returncode != 0:
            invalid_commands.append(command)

    if len(invalid_commands) > 0:
        # there are commands that can not be executed, stop job execution
        cloud_log(f'Can not execute commands! Following commands are invalid: {", ".join(set(invalid_commands))}', log_types["stderr"])
        global final_status; final_status = job_statuses["execution_error"]
        return

    # build command and execute as separate process
    start_and_monitor_job(["/bin/bash", "-c", commands], env_vars)


def run_decorator_job(env_vars):
    # Construct the command
    command_base = "pip install -r requirements.txt &&"
    entry_point = job['entryPoint']

    if entry_point is None:
        cloud_log('Entry point is required for decorator jobs!', log_types['stderr'])
        global final_status; final_status = job_statuses["execution_error"]
        return

    meta = job.get('meta', {})
    job_arguments = meta.get('jobArguments', [])

    # Join job arguments with spaces
    arguments_string = ' '.join(job_arguments)

    # Construct the execution command
    execution_command = f"python {entry_point} {arguments_string}"

    # Log the execution command
    cloud_log(f"Installing Dependencies and running: {execution_command}")

    # Combine the base command with the execution command
    full_command = f"{command_base} {execution_command}"

    # Final command to be used
    command = ["sh", "-c", full_command]
    start_and_monitor_job(command, env_vars)


def start_and_monitor_job(command, env_vars):
    # Start job

    # Copy current environment variables and update with custom env_vars
    env = os.environ.copy()
    
    if env_vars is not None:
        env.update(env_vars)

    global running_job; running_job = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True, cwd=working_dir, env=env)

    # Start parallel threads
    termination_thread = start_termination_thread()
    charge_thread = start_charging_thread()
    stdout_thread = Thread(target=logging_thread, args=(running_job.stdout, log_types["stdout"])); stdout_thread.start()
    stderr_thread = Thread(target=logging_thread, args=(running_job.stderr, log_types["stderr"])); stderr_thread.start()

    # Wait for the process to finish
    running_job.wait()

    # Terminate threads
    global kill_threads; kill_threads = True
    stdout_thread.join()
    stderr_thread.join()
    charge_thread.join()
    termination_thread.join()

    global return_code; return_code = running_job.returncode
    global final_status
    if final_status != job_statuses['terminated'] and return_code > 0: final_status = job_statuses["execution_error"]


# Upload results ----------------------------------------------------
def upload_result():
    try:
        cloud_log('Copying results')

        # Ensure the result directory exists
        os.makedirs(results_dir, exist_ok=True)
        # Copy workspace to result directory (uploads result to S3 bucket)
        subprocess.run(["cp", "-r", f"{working_dir}/.", results_dir], check=True)

        cloud_log('Results successfully copied')

    except subprocess.CalledProcessError as e:
        cloud_log(f'CalledProcessError: {e}', log_types["stderr"])
    except PermissionError as e:
        cloud_log(f'PermissionError: {e}', log_types["stderr"])
    except Exception as e:
        cloud_log(f'An error occurred: {e}', log_types["stderr"])


# Finish Job --------------------------------------------------------
def finish_job():
    # Collect outputs and finalize the job
    out_str = '\n'.join(stdout)
    err_str = '\n'.join(stderr)

    tokens_used = job['tokensUsed']

    if tokens_used:
        tokens_used_msg = f'Total tokens used for processing job: {tokens_used}'
        cloud_log(tokens_used_msg)
        out_str += tokens_used_msg

    update_job(status=final_status, end_date=datetime.now(timezone.utc), output_log=out_str, error_log=err_str)
    
    # Shared backend checks for this signal to terminate socket connection
    cloud_log("POSITRON_SIGNAL_EOS")


'''_______________________________________________________________________________________
    
    UTILS
    ______________________________________________________________________________________
'''
# Check for termination ---------------------------------------------
def is_job_active():
    resp = try_request(requests.get, API_GET_JOB, headers=headers)
    db_job = resp.json()
    inactive_statuses = [
        job_statuses["complete"],
        job_statuses["failed"],
        job_statuses["execution_error"],
        job_statuses["terminate"],
        job_statuses["terminated"],
    ]

    if db_job['status'] not in inactive_statuses:
        return True

    global final_status
    if db_job['status'] == job_statuses["terminate"]:
        final_status = job_statuses["terminated"]
        cloud_log("The job has been terminated by the user.")
    else:
        final_status = db_job['status']
        cloud_log(f"The job is not active anymore (status: {db_job['status']})")

    return False


# Update Job --------------------------------------------------------
def update_job(status, start_date=None, end_date=None, output_log=None, error_log=None):
    cloud_log(f'Updating status: {status}')
    body={
        "status": status,
        "startDate": start_date.isoformat() if start_date is not None else None,
        "endDate": end_date.isoformat() if end_date is not None else None,
        "outputLog": output_log,
        "errorLog": error_log
    }
    # filter out the items where the value is None
    body = {key:value for key, value in body.items() if value is not None}
    try_request(requests.post, API_UPDATE_JOB, headers=headers, json_data=body)

# Charging thread ---------------------------------------------------
def start_charging_thread():
    cloud_log('Start charging thread', log_types["debug"])
    def charge_thread():
        while not kill_threads:
            res = try_request(requests.post, API_JOB_LIFECYCLE, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if not j['succeeded']:
                # unable to validate job lifecycle due to known reason (e.g. insufficient funds, time/token limit exceeded)
                cloud_log('Job lifecycle error!', log_types["stderr"])
                cloud_log(j['message'], log_types["stderr"])

            # @Todo: discuss if job should be charged for every computational minute that is started, i.e. if termination occurs
            # between two charge calls, should we charge for the minute that was started but not completed?
            time.sleep(charge_interval) # @Todo: if these intervals are too long, termination of the job can take long
    ct = Thread(target=charge_thread)
    ct.start()
    return ct


# Termination thread ------------------------------------------------
def start_termination_thread():
    cloud_log('Starting termination thread', log_types["debug"])
    def termination_thread():
        while not kill_threads:
            res = try_request(requests.get, API_GET_JOB, headers=headers)
            if res is None:
                # stop looping, job is forced to terminate by try_request
                break
            j = res.json()
            if j['status'] == job_statuses['terminate']:
                cloud_log('Terminating job')
                terminate_running_job()
                global final_status; final_status = job_statuses["terminated"]
                break
            time.sleep(check_termination_interval)

    tt = Thread(target=termination_thread)
    tt.start()
    return tt


# Logging thread ----------------------------------------------------
def logging_thread(pipe, level):
    try: 
        with pipe:
            for line in pipe:
                if line.strip():
                    cloud_log(line.rstrip(), level)
    except:
        cloud_log(f'{level} logging pipe closed!')


# Terminate running job ---------------------------------------------
def terminate_running_job():
    global running_job
    # Signal termination
    running_job.stdout.close()
    running_job.stderr.close()
    running_job.kill()


# Print logs and send to cloud watch --------------------------------
def cloud_log(message: str, level = log_types["stdout"]):
    print(level, message)
    
    if level == log_types['stderr']: stderr.append(message)
    else: stdout.append(message)
    
    sys.stdout.flush()
    timestamp = int(round(time.time() * 1000))
    message = {'timestamp': timestamp, 'log_level': level, 'message': message, 'app_name': 'positron_wrapper'}
    log_events = [{
        'timestamp': timestamp,
        'message': json.dumps(message),
    }]

    log_group_name = os.getenv('AWS_JOB_LOG_GROUP_NAME')
    log_stream_name = f'positron-job-{job_id}'

    try:
        cloudwatch_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
    except Exception as e:
        print(f'Failed to submit logs: {e}')


# Retry API requests ------------------------------------------------
def try_request(request_func, url, retries=2, headers=None, json_data=None):
    for attempt in range(retries):
        try:
            response = request_func(url, headers=headers, json=json_data)
            response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
            return response
        except requests.RequestException as e:
            cloud_log(f"Attempt {attempt + 1} failed: {e}", log_types["debug"])
            if attempt < retries - 1:
                cloud_log("Retrying...", log_types["debug"])
                time.sleep(2)  # Adding a delay before retrying
            else:
                cloud_log("Max retries reached, terminating job.", log_types["debug"])
                terminate_running_job()
                return None


'''_______________________________________________________________________________________
    
    RUN!
    ______________________________________________________________________________________
'''
def run():
    try:
        # 1. Get the job details
        get_job()

        if is_job_active():
            # 2. Update status to initializing
            update_job(status=job_statuses["initializing"], start_date=datetime.now(timezone.utc))

            # 3. Unpack workspace tar
            if is_job_active():
                unpack_workspace()

                # 4. Run the job (including dependency install)
                if is_job_active():
                    run_job()

                    # 5. Update status to Storing
                    update_job(status=job_statuses['storing'])

                    # 6. Upload results
                    upload_result()

        # 7. Get the completed job details
        get_job()
        # 8. Update status to success or error
        finish_job()

    except Exception as e:
        cloud_log(f'An exception occured: {str(e)}', log_types["stderr"])

