
import logging
from cyclarity_sdk.platform_api.logger.models import ExecutionLog, LogInformation, LogPublisher


class ClarityStreamer(logging.Handler):
    def __init__(self, log_publisher: LogPublisher, execution_metadata):
        logging.Handler.__init__(self)
        self.log_publisher = log_publisher
        self.execution_metadata = execution_metadata

    def emit(self, record: logging.LogRecord) -> None:
        log_information = LogInformation(
            logger_name=record.name, log_level=record.levelno, time_stamp=record.created, message=record.message)
        execution_log = ExecutionLog(
            metadata=self.execution_metadata, data=log_information)
        try:
            self.log_publisher.publish_log(execution_log)
        except Exception as e:
            print("Failed publishing log topic, exception: " + str(e))
