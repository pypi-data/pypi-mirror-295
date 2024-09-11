
from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi   # noqa
from cyclarity_sdk.platform_api.logger.models import ExecutionLog, LogPublisher
from cyclarity_sdk.sdk_models.artifacts import TestArtifact
from cyclarity_sdk.sdk_models.findings import Finding
from cyclarity_sdk.sdk_models import ExecutionState
from clarity_common import ExecutionMetadata   # noqa
import requests


class RestConnector(IPlatformConnectorApi, LogPublisher):
    def __init__(self, execution_metadata: ExecutionMetadata, token, domain):  # noqa
        self.execution_metadata = execution_metadata
        self.domain = domain
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    def send_artifact(self, test_artifact: TestArtifact):
        url = f'{self.domain}/sdk-api/testing/artifacts'
        data = test_artifact.model_dump_json()
        response = requests.post(url, headers=self.headers, data=data)
        return response.status_code

    def send_finding(self, finding: Finding):
        url = f'{self.domain}/sdk-api/testing/findings'
        data = finding.model_dump_json()
        response = requests.post(url, headers=self.headers, data=data)
        return response.status_code

    def send_state(self, execution_state: ExecutionState):
        url = f'{self.domain}/sdk-api/testing/state'
        data = execution_state.model_dump_json()
        response = requests.post(url, headers=self.headers, data=data)
        return response.status_code

    def publish_log(self, execution_log: ExecutionLog):
        url = f'{self.domain}/sdk-api/testing/logs'  # TODO
        data = execution_log.model_dump_json()
        response = requests.post(url, headers=self.headers, data=data)
        return response.status_code

    def get_execution_meta_data(self) -> ExecutionMetadata:
        return self.execution_metadata

    def set_execution_meta_data(self, execution_metadata: ExecutionMetadata):
        self.execution_metadata = execution_metadata
