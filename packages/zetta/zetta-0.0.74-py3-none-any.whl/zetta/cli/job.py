# Copyright ZettaBlock Labs 2024
import typer
from typing import Optional
from typing_extensions import Annotated
from zetta._utils.cli_options import common_env_option
from zetta._utils.async_utils import synchronizer
from zetta._utils.blockchain import send_fine_tune_request, get_transaction_link
from zetta._utils.connections import check_api_status

from zetta.job import worker_get_job, worker_get_jobs, worker_log_job, worker_run_job, process_zetta_job_config, init_zetta_job_config, gitea_upload, create_model_if_not_exist

job_cli = typer.Typer(
    name="job", help="Build your models in Zetta Workspace.", no_args_is_help=True
)


@job_cli.command(name="list", help="List all build jobs that are currently running.")
@synchronizer.create_blocking
async def list(env: str=common_env_option(), json: bool = True):
    try:
        jobs = worker_get_jobs(env, json_output=json)
        print(jobs)
    except Exception as e:
        print(e)


@job_cli.command(name="get", help="get a job status.")
@synchronizer.create_blocking
async def get(jobid, env: str=common_env_option(), json: bool = True):
    try:
        job = worker_get_job(jobid, env, json_output=json)
        if job == 'null':
            print("No job record found matching with job id {}".format(jobid))
            return
        print(job)
    except Exception as e:
        print(e)


@job_cli.command(name="update", help="update a job.")
@synchronizer.create_blocking
async def update(json: bool = True):
    pass


@job_cli.command(name="cancel", help="cancel a running job for current user.")
@synchronizer.create_blocking
async def cancel(json: bool = True):
    pass


@job_cli.command(name="status", help="check the status of Zetta ai-network API.")
@synchronizer.create_blocking
async def status(env: str=common_env_option()):
    result = check_api_status(env)
    print(result['status'])
    return result


@job_cli.command(
    name="init", help="Initialize a new fine-tune job at designated location."
)
@synchronizer.create_blocking
async def init(
    project_name: Annotated[str, typer.Argument(..., help="Name of the project, which will be used as the default output model name.")],
    framework: str = "llama-factory",
    location: str = "."
):
    """
    Initialize a new fine-tune project with name `project_name`. A config template will be downloaded at designated file location.
    `project_name` is the default name of the fine-tune model.
    """
    if framework == "llama-factory":
        config_path = init_zetta_job_config(project_name, location)
        print(f"Created config file at {config_path}. Fill in and get started!")
    else:
        print(f"Framework {framework} is not supported.")
    pass


@job_cli.command(
    name="run", help="Create a new fine-tune job with given configuration."
)
@synchronizer.create_blocking
async def run(
    config: Annotated[str, typer.Argument(..., help="Path to the config file.")],
    env: str = common_env_option(),
    gpu: Annotated[Optional[str], typer.Option(..., help="Type of the GPU to use.")] = None,
    gpu_num: Annotated[Optional[str], typer.Option(..., help="Number of GPUs to use.")] = 1,
):
    """
    Submit a new fine-tune job with given config file and optional hardware requirements.
    `config` can be a local file path or a URL to a public GitHub repository with `config.yaml` file in the root.
    Return a job id.
    """
    # parse job config
    lf_config, output_model_name, zettablock_datasets = process_zetta_job_config(config)

    # send fine-tune request to blockchain
    print("Sending fine-tune request to blockchain...")
    try:
        events = send_fine_tune_request()
        if events is None or len(events) == 0:
            raise Exception("sendFineTuneRequest event not found")
        print(f"Job request is sent, check your transaction at {get_transaction_link(events[0].transactionHash.hex())}")
    except Exception as e:
        print(f"Warning: Failed to send fine-tune request: {e}")

    # initialize model repository
    model_repo_name = f"{output_model_name}"
    try:
        create_model_if_not_exist(model_repo_name)
    except Exception as e:
        print(f"Warning: Failed to initialize model repository. {e}")

    # submit job to ai-network
    try:
        resp = worker_run_job(lf_config, env, gitea_reponame=model_repo_name, zettablock_datasets=zettablock_datasets)
        job_id = resp["uuid"]
        print(f"Job submitted successfully. Your job id is \"{job_id}\".")
        # submit code to gitea
        commit_link = gitea_upload(config, job_id)
        # inform code commit link
        if commit_link is not None:
            print(f"Your files are snapshot at: {commit_link}")
        else:
            print("Warning: Failed to create code snapshot.")
        return resp
    except Exception as e:
        print(f"Failed to submit job: {e}")
        return None


@job_cli.command(name="logs", help="Show the logs of a job with given job id.")
@synchronizer.create_blocking
async def logs(job_id: str):
    try:
        job = worker_log_job(job_id)
        print(job)
    except Exception as e:
        print(e)
