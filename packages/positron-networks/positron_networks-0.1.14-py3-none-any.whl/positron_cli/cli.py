import typer
import configparser
import requests
import time
import os
import webbrowser
from positron_common.deploy import positron_deploy
from positron_common.config import get_job_config
from positron_common.cli_args import args
from positron_common.utils import debug as print_d
from . import run_job, login

app = typer.Typer(help="A CLI tool to help you run your code in the Positron Cloud")

app.command()(run_job)
app.command()(login)

# TODO:
# @app.command()
# def setEnv(env: str = 'dev') # local, dev, alpha, beta
# update config.ini with proper urls

if __name__ == "__main__":
    app()
