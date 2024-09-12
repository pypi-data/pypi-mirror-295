from typing import Any, Dict, List, Optional
import click
from rich import box
from rich.console import Console
from rich.table import Table

from .client import send_request


@click.group(name="gpu_machines")
def gpu_machines():
    """
    ScaleGen commands for managing fine-tuning deployments
    """
    pass


def get_available_machines(
    gpu_type: Optional[str], num_gpus: Optional[int]
) -> Optional[List[Dict[str, Any]]]:
    response = send_request(
        "GET",
        "/gpu_machines/list_available",
        params={
            "gpu_type": gpu_type,
            "num_gpus": num_gpus or 1 if gpu_type else num_gpus,
        },
    )
    if response.status_code != 200:
        click.echo(f"Error: {response.content.decode('utf-8')}")
        return
    return response.json()


@gpu_machines.command(name="list")
def list_gpu_machines():
    """
    List all GPU machines
    """
    response = send_request("GET", "/gpu_machines/list")
    gpu_machines = response.json()

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Machine ID")
    table.add_column("GPU Type x Count")
    table.add_column("Status")
    table.add_column("Region")

    for gpu_machine in gpu_machines:
        table.add_row(
            gpu_machine["id"],
            f'{gpu_machine["instance_details"]["gpu_type"]} x {gpu_machine["instance_details"]["gpu_count"]}',
            gpu_machine["status"],
            gpu_machine["instance_details"]["region"],
        )
    console.print(table)


# TODO: Add loading animation while fetching data
# TODO: Add command for Deleting GPU machines
# TODO: Create command for viewing GPU machines
@gpu_machines.command(name="view")
@click.argument("machine_id", type=click.STRING)
def view_gpu_machine(machine_id: str):
    """
    View a GPU machine
    """
    # Fetch data from the API
    # Download SSH Key
    # Display panel along with SSH command
    pass


@gpu_machines.command(name="list_available")
@click.option("--gpu_type", type=click.STRING, required=False, help="GPU Type to use")
@click.option(
    "--num_gpus", type=click.INT, required=False, help="Number of GPUs to use"
)
@click.option("-p", "--plain", is_flag=True)
def list_available_gpu_machines(
    gpu_type: Optional[str], num_gpus: Optional[int], plain: bool
):
    table = Table(
        show_header=True,
        title="Available GPU Machines",
        box=None if plain else box.DOUBLE_EDGE,
    )

    col_names = [
        "ID",
        "GPU Type",
        "GPU Count",
        "Price Per Hour (USD)",
        "Region",
        "Memory (GB)",
        "vCPUs",
    ]

    for col in col_names:
        table.add_column(col)

    data = get_available_machines(gpu_type, num_gpus)
    if not data:
        return

    for machine in data:
        table.add_row(
            machine["id"],
            machine["gpu_type"],
            str(machine["gpu_count"]),
            str(round(machine["on_demand"], 3)),
            machine["region"],
            str(int(machine["memory"])),
            str(int(machine["vcpus"])),
        )

    console = Console()

    if table.row_count <= 15 or plain:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")


@gpu_machines.command(name="create")
@click.option(
    "--machine_avail_id",
    type=click.STRING,
    required=True,
    help="Machine ID from list_available command",
)
@click.option(
    "--artifacts_store_name",
    type=click.STRING,
    required=False,
    help="Artifacts Store name to be used",
)
def create_gpu_machine(
    machine_avail_id: str,
    artifacts_store_name: Optional[str] = None,
):
    """
    Create a new GPU machine
    """

    payload: Dict[str, Any] = {
        "machine_avail_id": machine_avail_id,
        "artifacts_store_name": artifacts_store_name,
    }

    response = send_request("POST", "/gpu_machines/create", data=payload)
    if response.status_code == 200:
        click.echo(response.json())
    else:
        click.echo(f"Error: {response.content.decode('utf-8')}")
