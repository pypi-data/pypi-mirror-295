from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Self
from uuid import UUID

import httpx
from httpx import AsyncClient
from loguru import logger
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from exb_sdk.workflow_client._api_constants import (
    ENDPOINT_DOWNLOAD,
    ENDPOINT_STATE_POLL,
    ENDPOINT_UPLOAD,
    DocumentState,
)
from exb_sdk.workflow_client.exceptions import (
    DocumentProcessingError,
    HttpError,
    WaitForResultCancelledError,
)

if TYPE_CHECKING:
    from pathlib import Path
    from types import TracebackType

Result = dict[str, Any]


def _should_retry(exception: BaseException) -> bool:
    if isinstance(exception, HttpError):
        return exception.response.status_code in {500, 502, 503}
    return False  # pragma: no cover


def _on_retry_stop(retry: RetryCallState) -> None:
    # Avoid raising tenacity.RetryError
    http_error: HttpError = retry.outcome.exception()  # type: ignore[assignment, union-attr]
    raise http_error


@dataclass(kw_only=True)
class Client:
    """A client for getting results of a given document.

    Attributes:
        base_url: The base URL of the ExB app.
        customer_id: The customer ID of the solution.
        solution_id: The solution ID where the workflow exists.
        token: The API credential token used for authorization.
        dev_mode: When enabled allows to cache file upload and faster result polling. Useful
            during development when extracting results of the same file multiple times.
            Do not use when running this in production! Defaults to False.
    """

    base_url: str
    customer_id: UUID
    solution_id: UUID
    token: str
    dev_mode: bool = False

    _http_client: AsyncClient = field(init=False)
    _poll_interval: float = field(init=False)
    _max_connections: int = field(init=False, default=10)
    _closing: bool = False

    def __post_init__(self) -> None:
        self._poll_interval = 20 if self.dev_mode else 60
        self._http_client = self._create_http_client()
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)

    async def __aenter__(self) -> Self:
        if self._http_client.is_closed:
            self._http_client = self._create_http_client()
        self._closing = False
        return self

    def _create_http_client(self) -> AsyncClient:
        url = f"{self.base_url}/{self.customer_id}/{self.solution_id}/latest"
        limits = httpx.Limits(max_connections=self._max_connections)
        return AsyncClient(base_url=url, auth=("exb", self.token), limits=limits)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._closing = True
        await self._http_client.aclose()

    async def get_result(self, document_path: Path) -> Result:
        """Run an extraction in the ExB for the given document and return its result.

        Args:
            document_path: The path of the document to be uploaded and extracted.

        Raises:
            WaitForResultCancelledError: if the client gets closed while waiting for a result.
            DocumentProcessingError: if the extraction failed.
            HttpError: if any operation to upload or getting the result fails with an
                unexpected error.

        Returns:
            The result of the extraction as a dictionary.
        """
        # Upload file
        document_id = await self._upload_document(document_path=document_path)

        # Poll for result
        while True:
            await asyncio.sleep(self._poll_interval)
            if self._closing:
                raise WaitForResultCancelledError

            state = await self._get_state(document_id)
            if state == DocumentState.DOCUMENT_PROCESSED:
                break

            if state == DocumentState.PROCESSING_ERROR:
                raise DocumentProcessingError

        # Get result and return it
        return await self._download_result(document_id)

    @retry(
        retry=retry_if_exception(_should_retry),
        wait=wait_exponential(min=5, max=20),
        stop=stop_after_attempt(5),
        # TODO: use loguru more correctly  # noqa: FIX002
        before_sleep=before_sleep_log(logger, logging.DEBUG),  # type: ignore[arg-type]
        retry_error_callback=_on_retry_stop,
    )
    async def _upload_document(self, document_path: Path) -> UUID:
        with document_path.open("rb") as f:
            # let http client decide which mimetype it is
            files = {"file": f}
            response = await self._http_client.post(
                ENDPOINT_UPLOAD,
                files=files,
                timeout=30,
                params={
                    "keep_cache": self.dev_mode,
                },
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HttpError(message=str(e), response=e.response) from e

        document_id: str = response.json()[-36:]
        return UUID(document_id)

    async def _get_state(self, document_id: UUID) -> str:
        response = await self._http_client.get(ENDPOINT_STATE_POLL.format(document_id), timeout=10)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HttpError(message=str(e), response=e.response) from e

        state: str = response.json()["state"]
        return state

    async def _download_result(self, document_id: UUID) -> dict[str, Any]:
        response = await self._http_client.get(ENDPOINT_DOWNLOAD.format(document_id), timeout=30)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HttpError(message=str(e), response=e.response) from e

        result: Result = response.json()
        return result
