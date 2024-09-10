import click

from komo.agent.core import run, setup


@click.command("setup-and-run")
@click.option("--job-id", type=str, required=True)
@click.option("--setup-script", type=str, required=True)
@click.option("--run-script", type=str, required=True)
def cmd_setup_and_run(
    job_id: str,
    setup_script: str,
    run_script: str,
):
    setup(job_id, setup_script)
    run(job_id, run_script)
