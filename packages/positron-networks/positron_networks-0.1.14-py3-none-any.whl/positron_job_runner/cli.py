import typer
from .run_job import run

app = typer.Typer(help="Runs your job from the Positron Cloud environment.")

@app.command()
def hello():
    """
    Describes what you can do with the Positron Job Runner
    """
    print('Hello, I am the Positron Job Runner')
    print('Here is a list of thing I can help you with:')
    print('- Run a job in the Positron Cloud')

@app.command()
def run_job(job_id: str):
    """
    Run the job from inside a Positron container.

    Example usage:
    $ positron_job_runner run_job <job_id>
    """
    print('Running job in the Positron Cloud')
    print(f'Job ID: {job_id}')
    run()

if __name__ == "__main__":
    app()
