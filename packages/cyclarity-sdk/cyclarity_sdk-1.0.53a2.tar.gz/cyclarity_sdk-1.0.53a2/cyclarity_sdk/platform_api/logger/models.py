from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum
import logging
from typing import Union

from cyclarity_sdk.sdk_models import ExecutionMetadata, MessageType
from pydantic import BaseModel


class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class LogInformation(BaseModel):
    logger_name: str
    log_level: LogLevel
    time_stamp: datetime
    message: str


class ExecutionLog(BaseModel):
    '''All the needed attributes from logs to sent via mqtt'''
    metadata: ExecutionMetadata
    data: Union[LogInformation, dict]
    type: MessageType = MessageType.LOG


class LogPublisher(ABC):
    @abstractmethod
    def publish_log(self, execution_log: ExecutionLog):
        raise NotImplementedError(
            f'publish_log was not defined for class {self.__class__.__name__}')  # noqa
