import logging
import sys
import threading
from collections import deque
from time import sleep
from typing import IO

from .base import Job


class StreamCapture:
    def __init__(
        self, stream: IO[str], logger: logging.Logger, log_level: int = logging.INFO
    ) -> None:
        self.original_stream = stream
        self.logger = logger
        self.log_level = log_level

    def write(self, data: str) -> None:
        self.logger.log(self.log_level, data)
        self.original_stream.write(data)

    def flush(self) -> None:
        self.original_stream.flush()


class StreamToLogger:
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(
        self, logger: logging.Logger, log_level: int = logging.INFO, echo: bool = False
    ) -> None:
        self.logger: logging.Logger = logger
        self.log_level: int = log_level
        self.linebuf: str = ""
        self.echo: bool = echo

    def write(self, buf: str) -> None:
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
            # if self.echo:
            #     print(line.rstrip())

        self.flush()

    def flush(self) -> None:
        pass


class BufferedJobLogHandler(logging.Handler):
    def __init__(self, job: Job, flush_interval=5, buffer_size=10):
        super().__init__()
        self.job = job
        self.flush_interval = flush_interval
        self.buffer_size = buffer_size
        self.buffer = deque()
        self.lock = threading.Lock()
        self.flusher_thread = threading.Thread(
            target=self.flush_periodically, daemon=True
        )
        self.flusher_thread.start()

    def emit(self, record):
        with self.lock:  # type: ignore
            self.buffer.append(self.format(record))
            if len(self.buffer) >= self.buffer_size:
                self.flush_buffer()

    def flush_buffer(self):
        with self.lock:  # type: ignore
            while self.buffer:
                log_entry = self.buffer.popleft()
                # Instead of printing, append to the Job's logs
                self.job.log(log_entry)

    def flush_periodically(self):
        while True:
            sleep(self.flush_interval)
            if self.buffer:
                self.flush_buffer()
