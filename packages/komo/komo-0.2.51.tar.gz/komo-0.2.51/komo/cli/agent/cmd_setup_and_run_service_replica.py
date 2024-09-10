import click

from komo.agent.core import run_service_replica, setup_service_replica


@click.command("setup-and-run-service-replica")
@click.option("--service-id", type=str, required=True)
@click.option("--replica-id", type=int, required=True)
@click.option("--setup_script", type=str, required=True)
@click.option("--run_script", type=str, required=True)
def cmd_setup_and_run_service_replica(
    service_id: str,
    replica_id: int,
    setup_script: str,
    run_script: str,
):
    setup_service_replica(service_id, replica_id, setup_script)
    run_service_replica(service_id, replica_id, run_script)
