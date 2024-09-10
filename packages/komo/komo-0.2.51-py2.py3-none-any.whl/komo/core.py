import os
import shutil
import subprocess
import textwrap
import time
from typing import Dict, List, Optional

import yaml

from komo.api_client import KOMODO_JWT_TOKEN_FILE_PATH, APIClient
from komo.types import (
    ClientException,
    Cloud,
    Job,
    JobConfig,
    JobStatus,
    Machine,
    MachineConfig,
    MachineStatus,
    ReplicaStatus,
    Service,
    ServiceConfig,
    ServiceReplica,
    ServiceStatus,
    SSHInfoNotFound,
)


def login(api_key: str):
    if os.path.isfile(KOMODO_JWT_TOKEN_FILE_PATH):
        os.remove(KOMODO_JWT_TOKEN_FILE_PATH)
    komo_dir = os.path.expanduser("~/.komo")
    os.makedirs(komo_dir, exist_ok=True)
    api_key_file = os.path.join(komo_dir, "api-key")
    with open(api_key_file, "w") as f:
        f.write(api_key)


def launch_job(
    job_config: JobConfig,
    name: Optional[str] = None,
):
    api_client = APIClient()
    job = api_client.launch_job(
        job_config,
        name,
    )
    return job


def list_jobs() -> List[Job]:
    api_client = APIClient()
    jobs = api_client.get_jobs()
    return jobs


def get_job(job_id) -> Job:
    api_client = APIClient()
    job = api_client.get_job(job_id)
    return job


def print_job_logs(job_id, node_index: int = 0, follow: bool = False):
    api_client = APIClient()
    api_client.print_job_logs(job_id, node_index, follow)


def terminate_job(job_id):
    api_client = APIClient()
    api_client.terminate_job(job_id)


def _get_private_ssh_key() -> str:
    api_client = APIClient()
    ssh_key = api_client.get_private_ssh_key()
    return ssh_key


def ssh_job(job_id, node_index: int = 0):
    api_client = APIClient()

    job = api_client.get_job(job_id)

    if job.status not in [JobStatus.RUNNING, JobStatus.RUNNING_SETUP]:
        raise ClientException(f"Job {job_id} is not running")

    if node_index >= job.num_nodes:
        raise ClientException(
            f"Node index {node_index} is out of range for job {job_id} with"
            f" {job.num_nodes} node{'s' if job.num_nodes > 1 else ''}"
        )

    ssh_name = f"job-{job.id}"
    ssh_file = _update_ssh_config(ssh_name, job.ssh_info)

    ssh_node_name = ssh_name
    if node_index > 0:
        ssh_node_name = f"{ssh_node_name}-{job.ssh_info[node_index]['role']}"

    subprocess.call(
        [
            "ssh",
            "-t",
            ssh_node_name,
            f"cd ~/sky_workdir; bash --login",
        ]
    )

    os.remove(ssh_file)


def launch_machine(
    machine_config: MachineConfig,
    name: str,
) -> Machine:
    api_client = APIClient()
    machine = api_client.launch_machine(
        machine_config,
        name,
    )

    return machine


def list_machines() -> List[Machine]:
    api_client = APIClient()
    machines: List[Machine] = api_client.get_machines()

    running_machine_names = set(
        [m.name for m in machines if m.status == MachineStatus.RUNNING]
    )
    ssh_dir = os.path.expanduser("~/.komo/ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    for ssh_machine_name in os.listdir(ssh_dir):
        machine_name = ssh_machine_name[len("machine-") :]
        if machine_name not in running_machine_names:
            os.remove(os.path.join(ssh_dir, ssh_machine_name))

    return machines


def terminate_machine(machine_name: str):
    api_client = APIClient()
    machine = api_client.get_machine(machine_name, is_name=True)
    api_client.terminate_machine(machine.id)


def get_machine(machine_name: str) -> Machine:
    api_client = APIClient()
    machine = api_client.get_machine(machine_name, is_name=True)
    return machine


def _get_private_key_file():
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)
    key_file = os.path.join(ssh_dir, "komodo-key")
    if not os.path.isfile(key_file):
        ssh_key = _get_private_ssh_key()
        with open(key_file, "w") as f:
            f.write(ssh_key)
        os.chmod(key_file, 0o600)

    return key_file


def ssh_machine(machine_name):
    api_client = APIClient()

    machine = api_client.get_machine(machine_name, True)
    if machine.status not in [MachineStatus.RUNNING, MachineStatus.RUNNING_SETUP]:
        raise ClientException(f"Machine {machine_name} is not running")

    ssh_name = f"machine-{machine.name}"
    ssh_file = _update_ssh_config(ssh_name, [machine.ssh_info])

    subprocess.call(
        [
            "ssh",
            "-t",
            ssh_name,
            f"cd ~/sky_workdir; bash --login",
        ]
    )

    os.remove(ssh_file)


def _setup_ssh_config():
    ssh_config_file = os.path.expanduser("~/.ssh/config")
    include_entry = "Include ~/.komo/ssh/*\n"

    config = ""
    if not os.path.isfile(ssh_config_file):
        os.makedirs(os.path.expanduser("~/.ssh"), exist_ok=True)
    else:
        with open(ssh_config_file, "r") as f:
            config = f.read()

    if include_entry in config:
        return
    config = include_entry + config

    with open(ssh_config_file, "w") as f:
        f.write(config)


def _update_ssh_config(name: str, ssh_info: List[dict]):
    ssh_key_file = _get_private_key_file()

    ssh_commands = []
    for node_ssh_info in ssh_info:
        role = node_ssh_info["role"]
        if role == "head":
            ssh_name = name
        else:
            ssh_name = f"{name}-{role}"

        ip_address = node_ssh_info.get("ip_address", None)
        user = node_ssh_info.get("ssh_user", None)
        port = node_ssh_info.get("ssh_port", None)
        proxy_command = ""

        if not ip_address or not user or not port:
            raise SSHInfoNotFound()

        docker_user = node_ssh_info.get("docker_user", None)
        docker_port = node_ssh_info.get("docker_port", None)

        if docker_user and docker_port:
            proxy_command = f"ProxyCommand ssh -i {ssh_key_file} -o Port={port} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o ConnectTimeout=30s -o ForwardAgent=yes -W %h:%p {user}@{ip_address}"
            user = docker_user
            port = docker_port
            ip_address = "localhost"

        ssh_command = textwrap.dedent(
            f"""\
            Host {ssh_name}
                HostName {ip_address}
                User {user}
                IdentityFile {ssh_key_file}
                IdentitiesOnly yes
                ForwardAgent yes
                StrictHostKeyChecking no
                UserKnownHostsFile=/dev/null
                GlobalKnownHostsFile=/dev/null
                Port {port}
                {proxy_command}
        """.rstrip()
        )
        ssh_commands.append(ssh_command)

    ssh_file = os.path.expanduser(f"~/.komo/ssh/{name}")
    os.makedirs(os.path.expanduser("~/.komo/ssh"), exist_ok=True)
    with open(ssh_file, "w") as f:
        f.write("\n\n".join(ssh_commands))

    return ssh_file


def open_machine_in_vscode(machine_name):
    _setup_ssh_config()
    api_client = APIClient()

    code = shutil.which("code")
    if code is None:
        raise ClientException(
            "Please install the VSCode CLI"
            " (https://code.visualstudio.com/docs/editor/command-line)"
        )
    machine = api_client.get_machine(machine_name, is_name=True)
    if machine.status not in [MachineStatus.RUNNING, MachineStatus.RUNNING_SETUP]:
        raise ClientException(f"Machine {machine_name} is not running")

    ssh_name = f"machine-{machine.name}"
    _update_ssh_config(ssh_name, [machine.ssh_info])
    user = machine.ssh_info.get("docker_user", None) or machine.ssh_info["ssh_user"]
    if machine.ssh_info.get("docker_user", None) == "root":
        user = "/root"
    else:
        user = f"/home/{user}"

    subprocess.call(
        [
            "code",
            "--remote",
            f"ssh-remote+{ssh_name}",
            f"{user}/sky_workdir",
        ]
    )


def print_machine_setup_logs(machine_name: str, follow: bool):
    api_client = APIClient()
    machine = api_client.get_machine(machine_name, is_name=True)
    api_client.print_machine_setup_logs(machine.id, follow)


def list_services() -> List[Service]:
    api_client = APIClient()
    services = api_client.get_services()
    return services


def get_service(service_name: str) -> Service:
    api_client = APIClient()
    service = api_client.get_service(service_name, is_name=True)
    return service


def launch_service(
    service_config: ServiceConfig,
    name: str,
) -> Service:
    api_client = APIClient()
    service = api_client.launch_service(
        service_config,
        name,
    )

    return service


def terminate_service(
    service_name: str,
):
    api_client = APIClient()
    service = api_client.get_service(service_name, is_name=True)
    api_client.terminate_service(service.id)
