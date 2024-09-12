from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pytest

from exb_sdk.workflow_client import Client
from exb_sdk.workflow_client._api_constants import DocumentState  # noqa: PLC2701
from exb_sdk.workflow_client.exceptions import HttpError
from tests.workflow_client.conftest import Context, response_state, response_upload

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_httpx import HTTPXMock


@pytest.fixture
def client(ctx: Context) -> Client:
    c = Client(
        base_url=ctx.base_url,
        customer_id=ctx.customer_id,
        solution_id=ctx.solution_id,
        token="token",
    )
    c._poll_interval = 0.001  # noqa: SLF001
    return c


# FastAPI returns an object with extra information for validation errors, for example
ErrorDetails = list[dict[str, Any]]


@dataclass
class UnexpectedResponse:
    status_code: int
    detail: str | ErrorDetails


@pytest.mark.parametrize(
    ("response", "expected_message_match"),
    [
        (
            UnexpectedResponse(401, "Incorrect username or password"),
            "Client error '401 Unauthorized'",
        ),
        (
            UnexpectedResponse(404, "Solution not found"),
            "Client error '404 Not Found'",
        ),
        (
            UnexpectedResponse(422, "Filetype not acceptable audio/mpeg"),
            "Client error '422 Unprocessable Entity'",
        ),
    ],
)
async def test_unexpected_response_upload(
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
    response: UnexpectedResponse,
    expected_message_match: str,
) -> None:
    # arrange
    httpx_mock.add_response(status_code=response.status_code, json={"detail": response.detail})

    async with client:
        # assert
        with pytest.raises(HttpError, match=expected_message_match):
            # act
            await client.get_result(document_path=document_path)


async def test_unexpected_response_upload_retry_raises_http_error_after_stop_reached(
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(status_code=500, json={"detail": "Internal Server Error"})

    async with client:
        with pytest.raises(HttpError, match="Internal Server Error"):
            # act
            await client.get_result(document_path=document_path)


@pytest.mark.parametrize(
    ("response", "expected_message_match"),
    [
        (
            UnexpectedResponse(401, "Incorrect username or password"),
            "Client error '401 Unauthorized'",
        ),
        (
            UnexpectedResponse(404, "Solution not found"),
            "Client error '404 Not Found'",
        ),
        (
            UnexpectedResponse(
                422,
                [
                    {
                        "type": "uuid_parsing",
                        "loc": [
                            "path",
                            "solution_id",
                        ],
                        "msg": (
                            "Input should be a valid UUID, invalid length: expected length 32 "
                            "for simple format, found 3"
                        ),
                        "input": "abc",
                        "ctx": {
                            "error": (
                                "invalid length: expected length 32 for simple format, found 3"
                            ),
                        },
                    },
                    {
                        "type": "uuid_parsing",
                        "loc": [
                            "path",
                            "solution_id",
                        ],
                        "msg": (
                            "Input should be a valid UUID, invalid length: expected length 32 "
                            "for simple format, found 3",
                        ),
                        "input": "abc",
                        "ctx": {
                            "error": (
                                "invalid length: expected length 32 for simple format, found 3"
                            ),
                        },
                    },
                ],
            ),
            "Client error '422 Unprocessable Entity'",
        ),
        (
            UnexpectedResponse(500, "Internal server error"),
            "Server error '500 Internal Server Error'",
        ),
    ],
)
async def test_unexpected_response_state_poll(  # noqa: PLR0913, PLR0917
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
    response: UnexpectedResponse,
    expected_message_match: str,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(status_code=response.status_code, json={"detail": response.detail})

    async with client:
        # assert
        with pytest.raises(HttpError, match=expected_message_match):
            # act
            await client.get_result(document_path=document_path)


@pytest.mark.parametrize(
    ("response", "expected_message_match"),
    [
        (
            UnexpectedResponse(401, "Incorrect username or password"),
            "Client error '401 Unauthorized'",
        ),
        (
            UnexpectedResponse(404, "Solution not found"),
            "Client error '404 Not Found'",
        ),
        (
            UnexpectedResponse(
                422,
                [
                    {
                        "type": "uuid_parsing",
                        "loc": [
                            "path",
                            "solution_id",
                        ],
                        "msg": (
                            "Input should be a valid UUID, invalid length: expected length 32 "
                            "for simple format, found 3"
                        ),
                        "input": "abc",
                        "ctx": {
                            "error": (
                                "invalid length: expected length 32 for simple format, found 3"
                            ),
                        },
                    },
                    {
                        "type": "uuid_parsing",
                        "loc": [
                            "path",
                            "solution_id",
                        ],
                        "msg": (
                            "Input should be a valid UUID, invalid length: expected length 32 "
                            "for simple format, found 3",
                        ),
                        "input": "abc",
                        "ctx": {
                            "error": (
                                "invalid length: expected length 32 for simple format, found 3"
                            ),
                        },
                    },
                ],
            ),
            "Client error '422 Unprocessable Entity'",
        ),
        (
            UnexpectedResponse(500, "Internal server error"),
            "Server error '500 Internal Server Error'",
        ),
    ],
)
async def test_unexpected_response_result_download(  # noqa: PLR0913, PLR0917
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
    response: UnexpectedResponse,
    expected_message_match: str,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.PIPELINE_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.DOCUMENT_PROCESSED))
    httpx_mock.add_response(status_code=response.status_code, json={"detail": response.detail})

    async with client:
        # assert
        with pytest.raises(HttpError, match=expected_message_match):
            # act
            await client.get_result(document_path=document_path)
