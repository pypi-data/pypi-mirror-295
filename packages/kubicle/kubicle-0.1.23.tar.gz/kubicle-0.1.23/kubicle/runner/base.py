from abc import ABC, abstractmethod
from typing import Callable, TypeVar

from pydantic import BaseModel
from agentcore.models import V1UserProfile

from kubicle.base import Job

InputType = TypeVar("InputType", bound=BaseModel)
OutputType = TypeVar("OutputType", bound=BaseModel)


class JobRunner(ABC):
    """
    A base class for job runners.
    """

    @abstractmethod
    def run(self, fn: Callable[[InputType], OutputType], input: InputType) -> Job:
        pass

    @abstractmethod
    def refresh(self, job_id: str) -> Job:
        pass

    @abstractmethod
    def cancel(self, job_id: str) -> Job:
        pass


DEFAULT_OWNER_REF = V1UserProfile(email="anonymous@agentsea.ai")
