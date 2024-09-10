import os
import subprocess
import tempfile
import time
import traceback
import zipfile

import requests
from retry.api import retry_call

from komo.api_client import APIClient


class Logger:
    _TIME_BETWEEN_LOGS = 1

    def __init__(
        self,
        api_client: APIClient,
        task_id: str,
        task_type: str,
    ):
        self.api_client = api_client
        self.task_id = task_id
        self.task_type = task_type
        self.buffer = []
        self.last_log_time = None

    def flush(self):
        if len(self.buffer) == 0:
            return

        try:
            self.api_client.post_logs(
                self.task_id,
                self.task_type,
                self.buffer,
            )
        except Exception as e:
            print(e)
            traceback.print_exc()

        self.buffer = []
        self.last_log_time = time.time()

    def flush_if_necessary(self):
        curr_time = time.time()

        if (
            not self.last_log_time
            or (curr_time - self.last_log_time) > self._TIME_BETWEEN_LOGS
        ):
            self.flush()

    def log(self, message: str):
        self.flush_if_necessary()

        self.buffer.append(
            {
                "timestamp": int(time.time() * 1000),
                "message": message,
            }
        )

    def __del__(self):
        self.flush()


def _get_setup_node_index() -> int:
    node_index = os.environ.get("SKYPILOT_SETUP_NODE_RANK", 0)
    node_index = int(node_index)
    return node_index


def _get_node_index() -> int:
    node_index = os.environ.get("SKYPILOT_NODE_RANK", 0)
    node_index = int(node_index)
    return node_index


def _execute(
    api_client: APIClient,
    task_id: str,
    task_type: str,
    script: str,
    raise_on_error: bool = True,
):
    logger = Logger(api_client, task_id, task_type)

    with tempfile.TemporaryDirectory() as td:
        script_file = os.path.join(td, "script.sh")

        with open(script_file, "w") as f:
            f.write(script)

        proc = subprocess.Popen(
            ["bash", script_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        for line in proc.stdout:
            try:
                logger.log(line.decode("utf-8"))
            except:
                pass

        proc.communicate()
        if raise_on_error and proc.returncode != 0:
            raise Exception(f"Process exited with return code {proc.returncode}")


LAMBDA_LABS_CREDENTIALS_PATH = os.path.expanduser("~/.lambda_cloud/lambda_keys")
AWS_CREDENTIALS_PATH = os.path.expanduser("~/.aws/credentials")


def _cleanup_komodo_credentials():
    # Delete cloud credentials from the environment
    if os.path.exists(LAMBDA_LABS_CREDENTIALS_PATH):
        os.remove(LAMBDA_LABS_CREDENTIALS_PATH)


def __run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}\n{result.stderr}")
    return result.stdout


def _setup_external_traffic_policy(allowed_ports):
    try:
        # Reset ufw to default settings
        __run_command("sudo ufw --force reset")
        # Default policies: deny all incoming, allow all outgoing
        __run_command("sudo ufw default deny incoming")
        __run_command("sudo ufw default allow outgoing")
        # Always allow OpenSSH (port 22)
        __run_command("sudo ufw allow OpenSSH")
        # Allow the ports provided by Cloud Runner
        for port in allowed_ports:
            __run_command(f"sudo ufw allow {port}")

        # Enable UFW
        __run_command("sudo ufw --force enable")
        print("UFW setup complete.")
    except Exception as e:
        print(f"an error occurred while setting up the external traffic policy: {e}")
        raise e


def _setup_cluster_traffic_policy():
    """
    Allow all ports for the cluster nodes
    """
    is_komodo_cloud = os.environ.get("KOMODO_CLOUD", None) == "1"
    if not is_komodo_cloud:
        return

    cluster_node_ips = os.environ.get("SKYPILOT_NODE_IPS", "").split("\n")
    try:
        for ip in cluster_node_ips:
            print(f"Allowing all ports for {ip}")
            __run_command(f"sudo ufw allow from {ip}")
    except Exception as e:
        print(f"an error occurred while setting up the cluster traffic policy: {e}")
        raise e


def _setup_komodo_cloud():
    """
    Cleanup credentials and setup UFW for Komodo Cloud.
    """
    try:
        is_komodo_cloud = os.environ.get("KOMODO_CLOUD", None) == "1"
        if is_komodo_cloud:
            _cleanup_komodo_credentials()
            komodo_user_requested_ports_str = os.environ.get(
                "KOMODO_USER_REQUESTED_PORTS", "[]"
            )
            if (
                komodo_user_requested_ports_str == "[]"
                or komodo_user_requested_ports_str == ""
            ):
                komodo_user_requested_ports = []
            else:
                komodo_user_requested_ports = komodo_user_requested_ports_str.split(",")
            _setup_external_traffic_policy(komodo_user_requested_ports)
    except Exception as e:
        raise Exception(f"An error occurred while setting up Komodo Cloud: {e}")


def setup(job_id: str, setup_script: str):
    api_client = APIClient()
    node_index = _get_setup_node_index()
    try:
        _setup_komodo_cloud()
        api_client.mark_job_as_running_setup(job_id)
        task_id = f"{job_id}/{node_index}"
        _execute(api_client, task_id, "jobs", setup_script)
    except Exception as e:
        if node_index == 0:
            retry_call(api_client.finish_job, fargs=[job_id], tries=-1, delay=30)
        raise e


def run(job_id: str, run_script: str):
    api_client = APIClient()
    node_index = _get_node_index()
    try:
        _setup_cluster_traffic_policy()
        api_client.mark_job_as_running(job_id)
        task_id = f"{job_id}/{node_index}"
        _execute(api_client, task_id, "jobs", run_script)
    finally:
        if node_index == 0:
            retry_call(api_client.finish_job, fargs=[job_id], tries=-1, delay=30)


def setup_machine(machine_id: str, setup_script: str):
    api_client = APIClient()

    # Raise an error if Komodo Cloud setup fails since if it fails we may be leaking credentials or leaving
    # all ports open.
    try:
        _setup_komodo_cloud()
    except Exception as e:
        retry_call(api_client.terminate_machine, fargs=[machine_id], tries=-1, delay=30)
        raise e

    # We don't raise on error because we still want the machine to stay running even if the
    # setup script fails (so the user can debug)
    # TODO: instead of using raise_on_error=False, catch an exception, and mark the machine
    # as "setup failed" (will have to create this endpoint on the server)
    try:
        api_client.mark_machine_as_running_setup(machine_id)
        _execute(api_client, machine_id, "machines", setup_script, raise_on_error=False)
    finally:
        retry_call(
            api_client.mark_machine_as_running, fargs=[machine_id], tries=-1, delay=30
        )


def setup_service_replica(service_id: str, replica_id: int, setup_script: str):
    _setup_komodo_cloud()
    api_client = APIClient()
    task_id = f"{service_id}/{replica_id}"
    _execute(api_client, task_id, "services", setup_script)


def run_service_replica(service_id: str, replica_id: int, run_script: str):
    _setup_cluster_traffic_policy()
    api_client = APIClient()
    task_id = f"{service_id}/{replica_id}"
    _execute(api_client, task_id, "services", run_script)


def download_workdir(workdir_upload_id: str, destination: str):
    api_client = APIClient()
    os.makedirs(destination, exist_ok=True)

    download_url = api_client.get_workdir_download_url(workdir_upload_id)
    response = retry_call(
        requests.get,
        fargs=[download_url],
        tries=10,
        delay=3,
        backoff=1.2,
    )
    response.raise_for_status()
    tf = tempfile.mktemp()
    with open(tf, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(tf, "r") as zf:
        zf.extractall(destination)

    os.remove(tf)
