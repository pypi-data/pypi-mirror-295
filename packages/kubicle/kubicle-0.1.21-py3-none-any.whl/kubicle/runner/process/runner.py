from multiprocessing import Process
import time
import importlib
import inspect
import traceback
from typing import Callable
import os
import signal

from agentcore.models import V1UserProfile

from kubicle.base import Job, JobStatus, JobRuntime
from kubicle.runner.base import JobRunner, InputType, OutputType, DEFAULT_OWNER_REF
from kubicle.util import get_random_characters


def job_wrapper(module_name: str, function_name: str, input: InputType, job_id: str):  # type: ignore
    print("job wrapper..", flush=True)
    try:
        module = importlib.import_module(module_name)
        fn: Callable[[InputType], OutputType] = getattr(module, function_name)  # type: ignore
    except (ModuleNotFoundError, AttributeError) as e:
        error_message = f"Error loading function: {e}\n{traceback.format_exc()}"
        print(error_message, flush=True)
        save_job_error(job_id, error_message)
        return

    jobs = Job.find(id=job_id)
    if not jobs:
        error_message = f"Job {job_id} not found"
        print(error_message, flush=True)
        save_job_error(job_id, error_message)
        return
    job = jobs[0]

    try:
        print("calling function", flush=True)
        output = fn(input)
        print("function returned", flush=True)
        job.status = JobStatus.FINISHED
        job.result = output.model_dump_json()
        job.save()
    except Exception as e:
        error_message = (
            f"Error during function execution: {e}\n{traceback.format_exc()}"
        )
        print(error_message, flush=True)
        save_job_error(job_id, error_message)
    finally:
        job.refresh()
        job.finished = time.time()
        job.save()


def save_job_error(job_id: str, error_message: str):
    print("saving error...", flush=True)
    jobs = Job.find(id=job_id)
    if jobs:
        job = jobs[0]
        job.status = JobStatus.FAILED
        job.result = error_message
        job.finished = time.time()
        job.save()
        print("saved error", flush=True)


class ProcessJobRunner(JobRunner):
    """
    Process job runner
    """

    def __init__(self, owner_ref: V1UserProfile = DEFAULT_OWNER_REF) -> None:
        self.owner = owner_ref
        print("ProcessJobRunner.init()", flush=True)

    def run(self, fn: Callable[[InputType], OutputType], input: InputType) -> Job:
        print("ProcessJobRunner.run()", flush=True)
        run_fn_name = fn.__name__
        run_module = inspect.getmodule(fn).__name__  # type: ignore

        print(f"RUN_MODULE: {run_module}", flush=True)
        print(f"RUN_FN: {run_fn_name}", flush=True)
        print(f"INPUT: {input}", flush=True)
        print(f"OWNER: {self.owner}", flush=True)

        job_name = f"{run_fn_name}-{get_random_characters()}".lower().replace("_", "-")

        if not self.owner.email:
            raise Exception("Owner email is not set")

        job = Job(
            self.owner.email,
            JobStatus.RUNNING,
            JobRuntime.Process.value,
            job_name,
        )

        print("starting process...", flush=True)

        p = Process(
            target=job_wrapper,
            args=(run_module, run_fn_name, input, job.id),
        )
        p.daemon = True
        p.start()

        job.pid = p.pid
        job.save()

        return job

    def refresh(self, job_id: str) -> Job:
        # Find the job in the database or similar
        found = Job.find(id=job_id)
        if not found:
            raise ValueError(f"Job {job_id} not found")
        job = found[0]

        # Check if we have a stored PID and if the process is still running
        if job.pid:
            try:
                os.kill(job.pid, 0)  # Check if process is alive
                job.status = JobStatus.RUNNING
            except OSError:
                job.refresh()  # refresh the job status from the database
                if job.status != JobStatus.FINISHED:
                    job.status = JobStatus.FAILED
        else:
            job.status = JobStatus.FAILED

        job.save()
        return job

    def cancel(self, job_id: str) -> Job:
        # Find the job in the database or similar
        found = Job.find(id=job_id)
        if not found:
            raise ValueError(f"Job {job_id} not found")
        job = found[0]

        # Check if we have a stored PID and if the process is still running
        if job.pid:
            try:
                print(
                    f"Terminating process with PID {job.pid} for job {job_id}",
                    flush=True,
                )
                os.kill(job.pid, signal.SIGTERM)  # Send termination signal
                job.status = JobStatus.CANCELED
            except OSError:
                job.status = JobStatus.FAILED  # Process already finished or not found
        else:
            job.status = JobStatus.FAILED

        job.finished = time.time()
        job.save()

        return job
