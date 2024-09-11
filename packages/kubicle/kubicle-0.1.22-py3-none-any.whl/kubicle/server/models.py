from typing import Dict, List, Optional

from pydantic import BaseModel


class V1Job(BaseModel):
    id: str
    owner_id: str
    status: str
    runtime: str
    name: str
    namespace: Optional[str] = None
    logs: Optional[str] = None
    result: Optional[str] = None
    pid: Optional[int] = None
    created: float
    updated: float
    finished: float
    metadata: Dict[str, str] = {}


class V1Jobs(BaseModel):
    jobs: List[V1Job]
