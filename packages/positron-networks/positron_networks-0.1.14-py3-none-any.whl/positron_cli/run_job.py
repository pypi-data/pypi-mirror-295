import typer
from typing_extensions import Annotated
from positron_common.deploy import positron_deploy
from positron_common.config import get_job_config
from positron_common.cli_args import args

def run_job(
  config: Annotated[str, typer.Option(help='The path to the job configuration file')] = 'job_config.yaml',
  debug: Annotated[bool, typer.Option(help='Enable debug logging')] = False,
  stream_stdout: Annotated[bool, typer.Option(help='Stream the job\'s stdout back to your CLI')] = False
):
    """
    Run a Generic job in the Positron Cloud

    You need to define a job_config.yaml that defines the job you want to run.
    Make sure you run this script in the same directory as your file or provide the path to the job_config.yaml file.
    """
    print(f'Running a job with configuration file: {config}')

    args.init(debug=debug, stream_stdout=stream_stdout)
    job_config = get_job_config(config)
    positron_deploy(job_config)
