from enum import StrEnum


class DocumentState(StrEnum):
    """The possible states a document after uploading."""

    QUEUED_FOR_PROCESSING = "QUEUED_FOR_PROCESSING"
    PIPELINE_PROCESSING = "PIPELINE_PROCESSING"
    PROCESSING_ERROR = "PROCESSING_ERROR"
    DOCUMENT_PROCESSED = "DOCUMENT_PROCESSED"


ENDPOINT_UPLOAD = "/upload"
ENDPOINT_STATE_POLL = "/state/{}"
ENDPOINT_DOWNLOAD = "/result/{}/main"
