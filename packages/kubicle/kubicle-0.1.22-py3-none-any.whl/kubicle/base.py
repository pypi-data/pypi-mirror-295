import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, List, Optional

import shortuuid

from kubicle.db.conn import WithDB
from kubicle.db.models import JobRecord
from kubicle.server.models import V1Job


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"
    CANCELED = "canceled"
    UNKNOWN = "unknown"


class JobRuntime(Enum):
    K8s = "k8s"
    Process = "process"


@dataclass
class Job(WithDB):
    """A backgound job"""

    owner_id: str
    status: JobStatus
    runtime: str
    name: str
    id: str = field(default_factory=lambda: str(shortuuid.uuid()))
    namespace: Optional[str] = None
    logs: Optional[str] = None
    result: Optional[str] = None
    pid: Optional[int] = None
    created: float = field(default_factory=lambda: time.time())
    updated: float = field(default_factory=lambda: time.time())
    finished: float = field(default_factory=lambda: 0.0)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.save()

    def to_record(self) -> JobRecord:
        metadata_serialized = json.dumps(self.metadata)
        return JobRecord(
            id=self.id,
            owner_id=self.owner_id,
            status=self.status.value,
            name=self.name,
            runtime=self.runtime,
            namespace=self.namespace,
            logs=self.logs,
            pid=self.pid,
            result=self.result,
            created=self.created,
            updated=self.updated,
            finished=self.finished,
            metadata_=metadata_serialized,
        )

    @classmethod
    def from_record(cls, record: JobRecord) -> "Job":
        obj = cls.__new__(cls)
        obj.id = str(record.id)
        obj.owner_id = str(record.owner_id)
        obj.name = str(record.name)
        obj.status = JobStatus(str(record.status))
        obj.runtime = str(record.runtime)
        obj.namespace = record.namespace  # type: ignore
        obj.logs = record.logs  # type: ignore
        obj.pid = record.pid  # type: ignore
        obj.result = str(record.result)
        obj.created = record.created  # type: ignore
        obj.updated = record.updated  # type: ignore
        obj.finished = record.finished  # type: ignore
        obj.metadata = json.loads(str(record.metadata_)) if record.metadata_ else {}  # type: ignore
        return obj

    def to_v1(self) -> "V1Job":
        return V1Job(**asdict(self))

    @classmethod
    def from_v1(cls, schema: "V1Job") -> "Job":
        obj = cls.__new__(cls)
        obj.id = schema.id
        obj.owner_id = schema.owner_id
        obj.name = schema.name
        obj.status = JobStatus(schema.status)
        obj.runtime = schema.runtime
        obj.namespace = schema.namespace
        obj.logs = schema.logs
        obj.pid = schema.pid
        obj.result = schema.result
        obj.created = schema.created
        obj.updated = schema.updated
        obj.finished = schema.finished
        obj.metadata = schema.metadata
        return obj

    def log(self, message: str, add_timestamp=True) -> None:
        """Appends a log message to the job's logs, with an optional timestamp."""
        if add_timestamp:
            timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.gmtime())
            log_entry = f"{timestamp} {message}\n"
        else:
            log_entry = message + "\n"  # Assuming message is already formatted

        if not self.logs:
            self.logs = log_entry
        else:
            self.logs += log_entry

        self.updated = time.time()
        self.save()

    def save(self) -> None:
        for db in self.get_db():
            db.merge(self.to_record())
            db.commit()

    @classmethod
    def find(cls, **kwargs) -> List["Job"]:
        for db in cls.get_db():
            records = db.query(JobRecord).filter_by(**kwargs).all()
            return [cls.from_record(record) for record in records]

        raise SystemError("no session")

    @classmethod
    def delete(cls, id: str) -> None:
        for db in cls.get_db():
            record = db.query(JobRecord).filter_by(id=id).first()
            if record:
                db.delete(record)
                db.commit()

    def refresh(self) -> None:
        """
        Refreshes the instance's state based on the latest data from the database.
        """
        for db in self.get_db():
            record = db.query(JobRecord).filter_by(id=self.id).first()
            if not record:
                raise ValueError(f"No job found with id {self.id}")

            # Refreshing the instance attributes from the record
            self.owner_id = str(record.owner_id)
            self.name = str(record.name)
            self.status = JobStatus(str(record.status))
            self.runtime = str(record.runtime)
            self.namespace = record.namespace  # type: ignore
            self.logs = record.logs  # type: ignore
            self.result = str(record.result)
            self.created = record.created  # type: ignore
            self.updated = record.updated  # type: ignore
            self.finished = record.finished  # type: ignore
            self.metadata = (
                json.loads(str(record.metadata_)) if record.metadata_ else {}  # type: ignore
            )
