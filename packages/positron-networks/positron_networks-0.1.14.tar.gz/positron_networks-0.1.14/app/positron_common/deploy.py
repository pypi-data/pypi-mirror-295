from functools import wraps
import os
import requests
import tarfile
import asyncio
import socketio
from colorama import init, Fore
import time
import signal
import json
import sys
import re
from .utils import debug, PositronException
from .enums import log_types
from .env_config import env
from .config import PositronJob
from .cli_args import args as cli_args
from .job_api.create_job import CreateJobBody

# Initialize colorama
init(autoreset=True)

# Cloud deployment definition
def positron_deploy(job_config: PositronJob):
    signal.signal(signal.SIGINT, handle_sigint)
    debug(env)

    try:
        # TODO: Move to PositronJob
        print('Validating sync parameters')
        validate_sync_parameters(job_config=job_config)
        job_config.validate()
        debug(job_config)

        image_name = job_config.image
        environment_id = job_config.environment_id
        # TODO: move to PositronJob
        workspace_dir = (job_config.workspace_dir if job_config.workspace_dir else get_default_workspace_dir())
        debug(f'Workspace directory: {workspace_dir}')
        entry_point = job_config.entry_point
        max_tokens = job_config.max_tokens
        max_time = job_config.max_time

        print(f'Environment: {environment_id if environment_id else "<Default>"}')
        print(f'Image: {image_name if image_name else "<Default>"}')

        print('Creating workspace tar file')
        create_workspace_tar(workspace_dir=workspace_dir)

        print('Creating new job')
        job = create_job(job_config=job_config)
        debug(json.dumps(job, indent=4))
        environment_id=job['environmentName']

        print('Fetching presigned url for upload')
        resp = get_presigned_url(job_id=job['id'])

        print('Uploading compressed workspace to Positron storage')
        upload_file(resp.get('url'), resp.get('fields'))

        print('Starting Job')
        start_job(job_id=job['id'])

        print("Your workspace has been uploaded and the job is in a processing queue. Please check your dashboard to follow your jobs status!")
        print(f"\tJob Name: {job['name']} ({job['id']})")
        print(f"\tFunding Group: {job['fundingGroupName']} ({job['fundingGroupId']})")
        print(f"\tEnvironment: {environment_id} ({job['environmentId']})")

        start_stdout_stream(job['id'])
        
    except PositronException as e:
        print(e)
    except Exception as e:
        print('An exception occurred. Please use --debug flag to get details')
        debug(e)


# May be able to move all this login into JobConfig
def validate_sync_parameters(job_config: PositronJob):
    def try_parse_max_tokens(tokens):
        if tokens is None:
            return None, None
        try:
            token_amount = tokens if isinstance(tokens, int) else int(tokens)
        except:
            return None, f'{tokens} is not an integer!'
        if token_amount > 0:
            return token_amount, None
        else:
            return None, 'It must be a positive integer!'


    def try_parse_max_time(time_string):
        if time_string is None:
            return None, None
        matches = re.search(r'^(\d+):(\d{2})$', time_string)
        if matches is None:
            return None, 'Format must be HH:MM'
        try:
            hours = int(matches.group(1))
            minutes = int(matches.group(2))
        except:
            return None, 'Values must be integers!'
        if minutes >= 60:
            return None, 'Invalid minutes! Must be 0 <= minutes < 60!'
        return hours * 60 + minutes, None
        
    valid = True
    max_tokens, error = try_parse_max_tokens(job_config.max_tokens)
    if error is not None:
        print(f'Invalid maximum amount of tokens! {error}')
        valid = False
    job_config.max_tokens = max_tokens
    
    max_time, error = try_parse_max_time(job_config.max_time)
    if error is not None:
        print(f'Invalid maximum execution time! {error}')
        valid = False
    job_config.max_time = max_time

    if not valid:
        raise PositronException(
            'Validation failed! Please check your decorator parameters!')


def create_workspace_tar(workspace_dir: str = None):
    # Use the context manager to handle opening and closing the tar file
    with tarfile.open(env.COMPRESSED_WS_NAME, 'w:gz') as tar:
        for root, dirs, files in os.walk(workspace_dir):
            for exclude_dir in ['.venv', '.git', '__pycache__']:
                try:
                    dirs.remove(exclude_dir)
                except ValueError:
                    # Ignore if the directory is not in the list
                    pass
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, start=workspace_dir)
                file_size = os.path.getsize(full_path)
                tar.add(full_path, arcname=arcname)
                debug(f"Added {full_path} as {arcname}, size: {file_size} bytes")


def create_job(job_config: PositronJob):
    debug(f'Calling: {env.API_CREATE_JOB}')
    debug(job_config)
    data = CreateJobBody.from_config(job_config)
    debug(data.json())
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN}
    response = requests.post(env.API_CREATE_JOB, headers=Headers, json=data.json())
    debug(response)
    if response.status_code != 200:
        body = response.json()
        if body.get('userFriendlyErrorMessage'):
            print(body.get('userFriendlyErrorMessage'))
            debug(json.dumps(body, indent=2))
            raise PositronException('Cannot create job. Please resolve the issue and try again.')
        raise PositronException(
            f'Job creation failed with http code: {response.status_code} \n {response.text}')
    else:
        debug(response.json())
        return response.json()


def get_presigned_url(job_id):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    url = env.API_GET_PRESIGNED + '?filename=' + env.COMPRESSED_WS_NAME
    debug(f'Calling: {url}')
    response = requests.get(url, headers=Headers)
    debug(response)
    if response.status_code != 200:
        raise PositronException(
            f'Presigned url fetching failed with http code: {response.status_code} \n {response.text}')
    else:
        debug(response.json())
        return response.json()


def upload_file(url, data):
    with open(env.COMPRESSED_WS_NAME, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, data=data, files=files)
        if response.status_code != 204:
            raise PositronException(
                f'Upload failed with http code: {response.status_code} \n {response.text}')


def start_job(job_id):
    Headers = {"PositronAuthToken": env.USER_AUTH_TOKEN, "PositronJobId": job_id}
    debug(f'Calling: {env.API_START_JOB}')
    response = requests.get(env.API_START_JOB, headers=Headers)
    debug(response)
    if response.status_code != 200:
        raise PositronException(
            f'Failed to start job with http code: {response.status_code} \n {response.text}')
    else:
        debug(response.json())
        return response.json()


def start_stdout_stream(job_id):
    if cli_args.stream_stdout:
        try:
            asyncio.get_event_loop().run_until_complete(start_stream(job_id))
        except Exception as e:
            print (e)


sio = socketio.AsyncClient()


@sio.event(namespace='/stdout-stream')
async def connect():
    print('Connected to stdout stream')


@sio.event(namespace='/stdout-stream')
async def message(message):
    try:
        log = json.loads(message)
        if log['log_level'] == log_types['stdout']:
            print(Fore.GREEN + log['message'])
        elif log['log_level'] == log_types['stderr']:
            print(Fore.RED + log['message'])
        elif log['log_level'] == log_types['debug']:
            print(Fore.BLUE + log['message'])            
    except:
        print(message)


@sio.event(namespace='/stdout-stream')
async def disconnect():
    print('Disconnected from stdout stream')


@sio.event(namespace='/stdout-stream')
async def error(err):
    print('An error occured in the streaming process')
    debug(err)


async def start_stream(job_id):
    custom_headers = {
        "PositronAuthToken": env.USER_AUTH_TOKEN,
        "PositronJobId": job_id
    }
    await sio.connect(env.SOCKET_IO_DOMAIN, headers=custom_headers, socketio_path=env.SOCKET_IO_PATH)
    await sio.wait()


def handle_sigint(signum, frame):
    print('Terminating gracefully...')
    time.sleep(5)
    exit(0)

def get_default_workspace_dir():
    cwd = os.getcwd()
    # decorator path calculation from file being run
    dirname = os.path.dirname(sys.argv[0])
    # TODO: cli and decorator calculate the workspace dir differently
    # think about moving this logic into those packages.
    # Run from current directory for generic jobs
    if (sys.argv[1] == 'run-job'):
        dirname = ''
    normalized_dir = os.path.normpath(dirname)
    absolute_path = os.path.join(cwd, normalized_dir)
    return os.path.normpath(absolute_path)
