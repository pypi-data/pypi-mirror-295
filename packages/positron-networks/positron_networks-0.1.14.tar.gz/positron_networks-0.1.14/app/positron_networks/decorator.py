from functools import wraps
import sys
import os
import argparse
from positron_common.utils import debug
from positron_common.deploy import positron_deploy
from positron_common.config import PositronJob, get_job_config, merge_config
from positron_common.cli_args import args as cli_args

# Decorator definition
def positron_sync(**positron_parameters):

    # Parse command line arguments
    parser = argparse.ArgumentParser(description = "A decorator to handle deploying your code into the cloud")
    parser.add_argument('-l', '--local', action='store_true', help='Run your script locally', dest='local')
    parser.add_argument('--positron-deploy', action='store_true', help='Deploy your script into Positron Cloud', dest='deploy')
    parser.add_argument('--stream-stdout', action='store_true', help='Stream the stdout from Positron Cloud back to your cli', dest='stream_stdout')
    parser.add_argument('--debug', action='store_true', help='Get more detailed error messages', dest='debug')
    positron_args, job_args = parser.parse_known_args()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cli_args.init(
                local=positron_args.local,
                deploy=positron_args.deploy,
                stream_stdout=positron_args.stream_stdout,
                debug=positron_args.debug,
                job_args=job_args,
            )

            # get decorator parameters
            job_config_decorator = PositronJob(**positron_parameters)
            job_config = job_config_decorator

            # use job yaml as base if it exists
            job_config_yaml = get_job_config()
            if job_config_yaml:
                job_config = merge_config(job_config_yaml, job_config_decorator)

            # Need to ensure entry_point is set
            if not job_config.entry_point:
                job_config.entry_point = os.path.basename(sys.argv[0])

            # ensure valid config to run the job
            debug(job_config)
            job_config.validate()

            if cli_args.deploy:
                positron_deploy(job_config)
            elif cli_args.local or os.getenv('POSITRON_CLOUD_ENVIRONMENT', False):
                func(*args, **kwargs)
            else:
                parser.print_help()

        return wrapper
    return decorator
