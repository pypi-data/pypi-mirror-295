from typing import Optional
from pydantic import BaseModel

from cyclarity_sdk.sdk_models.types import ExecutionStatus  # noqa

# from common.models.common_models.models import ExecutionMetadata
from clarity_common import ExecutionMetadata
''' Test step definitions'''


class ExecutionState(BaseModel):
    '''Data structure to be send via topic::execution-state'''
    execution_metadata: ExecutionMetadata
    percentage: int
    status: ExecutionStatus
    error_message: Optional[str]
