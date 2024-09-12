import click
import os
import subprocess
import requests
from typing import Optional
import re

from nema.utils.global_config import GLOBAL_CONFIG, GlobalConfig, GlobalConfigWorkflow
from nema.workflow.workflow import Workflow
from nema.connectivity.connectivity_manager import save_auth_data

NEMA_PATH = os.path.expanduser("~/.nema")
AUTH_PATH = os.path.join(NEMA_PATH, "auth")


def authenticate_user(username, password):

    # Authenticate the user
    if GLOBAL_CONFIG.is_set:

        tenant_url = GLOBAL_CONFIG.tenant_api_url

        login_url = f"{tenant_url}/authentication/login"

    else:
        raise Exception(
            "There is no nema.toml file in this directory. Please run `nema init` to create one."
        )

    # Make a request to the login URL
    response = requests.post(
        login_url, json={"username": username, "password": password}
    )

    if not response.ok:
        if response.status_code == 401:
            print("Invalid credentials")
        else:
            print(response.status_code, response.text)
            print("Failed to login")
        return None

    # save the authentication and refresh token to the home directory
    response_data = response.json()
    tokens = response_data["tokens"]
    refresh_token = tokens["refresh_token"]
    access_token = tokens["access_token"]

    # create the directory if it does not exist
    save_auth_data(refresh_token=refresh_token, access_token=access_token)

    print("Login successful \U00002705")


@click.group()
def cli():
    pass


@cli.command()
def login():
    """Login to Nema."""
    username = click.prompt("Please enter your username or email address")
    password = click.prompt("Please enter your password", hide_input=True)
    authenticate_user(username, password)


@cli.command()
def init():
    "Initialize nema.toml file"
    print("Initializing nema.toml file")

    new_global_config = GlobalConfig()

    new_global_config.project_url = click.prompt(
        "Please enter the project URL", type=str
    )

    new_workflow_key = click.prompt(
        "Please enter a workflow identifier (this is only used locally)",
        type=str,
        default="my-first-workflow",
    )
    new_workflow_name = click.prompt(
        "Please enter a name for the workflow", type=str, default=new_workflow_key
    )
    new_workflow_description = click.prompt(
        "Please enter a workflow description",
        type=str,
        default="A Python workflow",
    )

    new_workflow = GlobalConfigWorkflow(
        key=new_workflow_key,
        name=new_workflow_name,
        description=new_workflow_description,
        command=["python", "main.py"],
    )

    new_global_config.workflows[new_workflow_key] = new_workflow

    new_global_config.save()


@cli.group()
def workflow():
    pass


@workflow.command()
@click.argument("identifier", required=False)
def init(identifier: Optional[str]):
    "Create a new workflow"

    if identifier is None:
        all_identifiers = GLOBAL_CONFIG.workflows.keys()
    else:
        print("Initializing all workflows")
        all_identifiers = [identifier]

    for this_identifier in all_identifiers:
        print(f"Initializing workflow with identifier '{this_identifier}'")
        existing_workflow = GLOBAL_CONFIG.workflows[this_identifier]

        if existing_workflow.global_id > 0:
            print("Workflow already exists. Skipping.")
            continue

        workflow = Workflow(
            global_id=0,
            name=existing_workflow.name,
            description=existing_workflow.description,
        )

        global_id = workflow.create()
        print(f"Workflow successfully created with global id {global_id}. \U00002705")

        existing_workflow.global_id = global_id

    # save the global ID to the config file
    GLOBAL_CONFIG.save()


@workflow.command()
@click.argument("identifier", required=False)
def run(identifier: Optional[str]):
    "Run the workflow"
    if identifier is None:
        all_identifiers = GLOBAL_CONFIG.workflows.keys()
    else:
        print("Initializing all workflows")
        all_identifiers = [identifier]

    for this_identifier in all_identifiers:
        print(f"Running workflow with identifier '{this_identifier}'")

        existing_workflow = GLOBAL_CONFIG.workflows[this_identifier]

        # run the python file
        subprocess_result = subprocess.run(
            existing_workflow.command, capture_output=True, text=True
        )
        print(subprocess_result.stdout)
        if subprocess_result.returncode == 0:
            output = subprocess_result.stdout

            match = re.search(r"Nema output written to folder: (.+)", output)
            if match:
                output_folder = match.group(1)
            else:
                print("Output data folder not found in the output. Exiting.")
                return
        else:
            print(f"Error: {subprocess_result.stderr}")
            return  # exit the function if the subprocess failed

        # process the update and submit to Nema
        workflow = Workflow(
            global_id=existing_workflow.global_id,
            name=existing_workflow.name,
            description=existing_workflow.description,
            output_folder=output_folder,
        )

        workflow.process_update()

        print(
            f"Workflow '{this_identifier}' successfully run \U0001F680 and results uploaded to Nema. \U00002705"
        )


if __name__ == "__main__":
    cli()
