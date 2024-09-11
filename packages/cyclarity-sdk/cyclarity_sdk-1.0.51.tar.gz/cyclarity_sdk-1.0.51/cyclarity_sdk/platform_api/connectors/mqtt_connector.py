import sys
from typing import Callable
from awsiot import mqtt_connection_builder
from awscrt import mqtt
from pydantic import BaseModel
from cyclarity_sdk.platform_api.logger.models import ExecutionLog, LogPublisher
from clarity_common import ExecutionMetadata
from cyclarity_sdk.sdk_models.artifacts import TestArtifact
from cyclarity_sdk.sdk_models import ExecutionState
from cyclarity_sdk.sdk_models.findings import Finding
from cyclarity_sdk.platform_api.Iplatform_connector import IPlatformConnectorApi   # noqa


class MqttConfig(BaseModel):
    endpoint: str
    port: int
    cert: str
    key: str
    ca: str
    client_name: str
    client_id: str
    on_connection_interrupted: Callable = None
    on_connection_resumed: Callable = None
    on_connection_success: Callable = None
    on_connection_failure: Callable = None


class MqttConnector(IPlatformConnectorApi, LogPublisher):
    '''
    This class is responsable for creating MQTT connection and MQTT Topics
    '''

    TOPICS = {
        "REQUEST_UPLOAD_LINK_TOPIC": "in-vehicle-scanner/get-upload-link/",
        "RECEIVE_UPLOAD_LINK_TOPIC": "in-vehicle-scanner/receive-upload-link/",
        "FINDINGS_TOPIC": "in-vehicle-scanner/push-findings/",
        "LOG_TOPIC": "in-vehicle-scanner/push-logs/",
        "STATE_UPDATE_TOPIC": "in-vehicle-scanner/state/",
        "SCAN_TEST_ARTIFACT_TOPIC": "in-vehicle-scanner/push-test-artifacts/",
        "STOP_EXECUTION": "in-vehicle-scanner/stop-execution/"
    }

    def __init__(self, config: MqttConfig, execution_metadata: ExecutionMetadata):  # noqa
        self.config = config
        self.execution_metadata = execution_metadata

        self.mqtt_connection, self.connect_future = self._create_mqtt_connection(  # noqa
            self.config.on_connection_interrupted, self.config.on_connection_resumed,  # noqa
            self.config.on_connection_success, self.config.on_connection_failure  # noqa
        )

    def get_execution_meta_data(self) -> ExecutionMetadata:
        return self.execution_metadata

    def set_execution_meta_data(self, execution_metadata: ExecutionMetadata):
        self.execution_metadata = execution_metadata

    def _create_mqtt_connection(self,
                                on_connection_interrupted=None,
                                on_connection_resumed=None,
                                on_connection_success=None,
                                on_connection_failure=None
                                ):  # noqa
        # Set default callbacks if not provided
        on_connection_interrupted = on_connection_interrupted if on_connection_interrupted is None else self._on_connection_interrupted   # noqa
        on_connection_resumed = on_connection_resumed if on_connection_resumed is not None else self._on_connection_resumed  # noqa
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=self.config.endpoint,
            port=self.config.port,
            cert_filepath=self.config.cert,
            pri_key_filepath=self.config.key,
            ca_filepath=self.config.ca,
            on_connection_interrupted=on_connection_interrupted,
            on_connection_resumed=on_connection_resumed,
            on_connection_success=on_connection_success,
            on_connection_failure=on_connection_failure,
            client_id=self.config.client_name,
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None,
        )
        connect_future = mqtt_connection.connect()
        connect_future.result()

        return mqtt_connection, connect_future

    def _on_connection_interrupted(self, connection, error, **kwargs):
        print(f"Connection interrupted. error: {error}")

    # Callback when an interrupted connection is re-established.
    def _on_connection_resumed(self, connection, return_code, session_present, **kwargs):  # noqa
        print(
            f"Connection resumed. return_code: {return_code} session_present:"
            f" {session_present}"
        )
        if return_code == 0 and not session_present:  # noqa
            print("Session did not persist. Resubscribing to existing topics...")  # noqa
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because
            # we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(self._on_resubscribe_complete)

    def _on_resubscribe_complete(self, resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print(f"Resubscribe results: {resubscribe_results}")

        for topic, qos in resubscribe_results["topics"]:
            if qos is None:
                sys.exit(f"Server rejected resubscribe to topic: {topic}")

    def publish(self, topic, payload):
        topic = topic + self.config.client_id
        future_result, packet_id = self.mqtt_connection.publish(
            topic=topic, payload=payload, qos=mqtt.QoS.AT_LEAST_ONCE
        )
        return future_result.result()

    def subscribe(self, topic, on_message_received: Callable):
        topic = topic + self.config.client_id
        subscribe_future, packet_id = self.mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_message_received,
        )
        return subscribe_future.result()

    def publish_log(self, execution_log: ExecutionLog):
        return self.publish(topic=MqttConnector.TOPICS['LOG_TOPIC'],
                            payload=execution_log.model_dump_json())

    def publish_finding(self, finding: Finding):
        return self.publish(topic=MqttConnector.TOPICS['FINDINGS_TOPIC'],
                            payload=finding.model_dump_json())

    def publish_execution_state(self, execution_state: ExecutionState):
        return self.publish(topic=MqttConnector.TOPICS['STATE_UPDATE_TOPIC'],
                            payload=execution_state.model_dump_json())

    def publish_artifact(self, test_artifact: TestArtifact):
        return self.publish(topic=MqttConnector.TOPICS['SCAN_TEST_ARTIFACT_TOPIC'],
                            payload=test_artifact.model_dump_json())

    def publish_result(self, res):
        return self.publish(topic=MqttConnector.TOPICS['REQUEST_UPLOAD_LINK_TOPIC'],
                            payload=res)

    def subscribe_upload_link_topic(self, on_message_received: Callable):
        return self.subscribe(topic=MqttConnector.TOPICS['RECEIVE_UPLOAD_LINK_TOPIC'],
                              on_message_received=on_message_received)

    def subscribe_stop_execution(self, on_message_received: Callable):
        return self.subscribe(topic=MqttConnector.TOPICS['STOP_EXECUTION'],
                              on_message_received=on_message_received)

    # IPlatformApi:
    def send_artifact(self, test_artifact: TestArtifact):
        return self.publish_artifact(test_artifact)

    def send_finding(self, finding: Finding):
        return self.publish_finding(finding)

    def send_state(self, execution_state: ExecutionState):
        return self.publish_execution_state(execution_state)
