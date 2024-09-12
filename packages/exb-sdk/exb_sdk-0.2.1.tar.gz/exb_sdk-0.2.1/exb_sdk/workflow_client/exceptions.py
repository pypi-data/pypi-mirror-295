from httpx import Response


class DocumentProcessingError(Exception):
    """Raised when an error occurs during an extraction."""

    def __init__(self) -> None:  # noqa: D107
        message = "Error processing document"
        super().__init__(message)


class HttpError(Exception):
    """Raised when an HTTP unhandled error is returned by the app."""

    def __init__(self, message: str, response: Response) -> None:  # noqa: D107
        super().__init__(message)
        self.response = response


class WaitForResultCancelledError(Exception):
    """Raised when the client is closed while extractions are running."""

    def __init__(self) -> None:  # noqa: D107
        message = "Wait for result cancelled for document"
        super().__init__(message)
