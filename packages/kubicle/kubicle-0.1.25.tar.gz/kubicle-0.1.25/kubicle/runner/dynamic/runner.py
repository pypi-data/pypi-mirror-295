import os
from typing import Optional, Dict, List

from agentcore.models import V1UserProfile

from kubicle.runner.base import JobRunner, DEFAULT_OWNER_REF


def DynamicRunner(
    local: bool = False,
    namespace: Optional[str] = None,
    owner_ref: V1UserProfile = DEFAULT_OWNER_REF,
    img: Optional[str] = None,
    envs: Dict[str, str] = {},
    include_env: List[str] = [],
    copy_env: bool = False,
    copy_exclude: Optional[List[str]] = None,
    service_account: str = "default",
) -> JobRunner:
    """
    Returns a JobRunner that dynamically loads a module and function at runtime.
    """

    from kubicle.runner.k8s.runner import K8sJobRunner
    from kubicle.runner.process.runner import ProcessJobRunner

    is_local = os.getenv("JOB_LOCAL")
    if is_local:
        if is_local.lower() == "true":
            local = True

    if local:
        print("using local runner", flush=True)
        return ProcessJobRunner(owner_ref=owner_ref)
    else:
        print("using k8s runner", flush=True)
        return K8sJobRunner(
            namespace=namespace,
            owner_ref=owner_ref,
            img=img,
            envs=envs,
            include_env=include_env,
            copy_env=copy_env,
            copy_exclude=copy_exclude,
            service_account=service_account,
        )
