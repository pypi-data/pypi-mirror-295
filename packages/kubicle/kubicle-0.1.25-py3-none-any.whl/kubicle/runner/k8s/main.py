import importlib
import json
import os
import inspect
from typing import Callable, Type

from pydantic import BaseModel
from agentcore.models import V1UserProfile

from kubicle.base import Job, JobStatus


def dynamic_import(module_name: str, function_name: str):
    """
    Dynamically imports a module and retrieves the specified function.

    Args:
        module_name: The name of the module to import.
        function_name: The name of the function to retrieve.

    Returns:
        The requested function.
    """
    module = importlib.import_module(module_name)
    return getattr(module, function_name)


if __name__ == "__main__":
    job_id = os.getenv("JOB_ID")
    if not job_id:
        raise ValueError("JOB_ID env var not set")
    print(f"JOB_ID: {job_id}")

    owner_json = os.getenv("OWNER_JSON")
    if not owner_json:
        raise ValueError("OWNER_JSON env var not set")
    owner = V1UserProfile.model_validate(json.loads(owner_json))
    print(f"OWNER: {owner.model_dump_json()}")

    print("finding job...")
    jobs = Job.find(id=job_id, owner_id=owner.email)
    if not jobs:
        raise ValueError(f"Job {job_id} not found")
    job = jobs[0]
    print("found job")

    print("getting module and function names")
    run_module_name = os.getenv("RUN_MODULE")
    run_fn_name = os.getenv("RUN_FN")
    if not run_module_name or not run_fn_name:
        raise ValueError("RUN_MODULE and RUN_FN env vars must be set")

    print(f"importing {run_fn_name} from {run_module_name}")
    run_fn = dynamic_import(run_module_name, run_fn_name)

    print("getting input model type")

    def get_input_model(fn: Callable) -> Type[BaseModel]:
        signature = inspect.signature(fn)
        parameters = signature.parameters
        for param in parameters.values():
            if issubclass(param.annotation, BaseModel):
                return param.annotation
        raise TypeError("No valid Pydantic model found in the function signature.")

    input_model_type = get_input_model(run_fn)

    print("getting model json")
    model_json = os.getenv("INPUT_JSON")
    if not model_json:
        raise ValueError("INPUT_JSON env var not set")

    input = input_model_type.model_validate(json.loads(model_json))
    print(f"MODEL: {input.model_dump_json()}")

    job.status = JobStatus.RUNNING
    job.save()

    try:
        output: BaseModel = run_fn(input)
    except Exception as e:
        print(f"failed to run job: {e}")
        job.status = JobStatus.FAILED
        job.result = str(e)
        job.save()
        raise e

    job.status = JobStatus.FINISHED
    job.result = output.model_dump_json()
    job.save()
