from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest

from exb_sdk.workflow_client import Client
from exb_sdk.workflow_client._api_constants import DocumentState  # noqa: PLC2701
from exb_sdk.workflow_client.exceptions import DocumentProcessingError, WaitForResultCancelledError
from tests.workflow_client.conftest import Context, response_result, response_state, response_upload

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


async def test_get_result(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.PIPELINE_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.DOCUMENT_PROCESSED))
    httpx_mock.add_response(**response_result(ctx=ctx, result={"foo": "bar"}))

    async with client:
        # act
        result = await client.get_result(document_path=document_path)

    # assert
    assert result == {"foo": "bar"}


async def test_get_result_retry(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(status_code=500, json={"detail": "Internal server error"})
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.PIPELINE_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.DOCUMENT_PROCESSED))
    httpx_mock.add_response(**response_result(ctx=ctx, result={"foo": "bar"}))

    async with client:
        # act
        result = await client.get_result(document_path=document_path)

    # assert
    assert result == {"foo": "bar"}


async def test_error_in_processing(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.PROCESSING_ERROR))

    async with client:
        # assert
        with pytest.raises(DocumentProcessingError, match="Error processing document"):
            # act
            await client.get_result(document_path=document_path)


async def test_get_result_httpx_client_lifecycle(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.PIPELINE_PROCESSING))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.DOCUMENT_PROCESSED))
    httpx_mock.add_response(**response_result(ctx=ctx, result={"foo": "bar"}))

    # act
    async with client:
        # Make a first request to actually "open" the httpx client
        await client.get_result(document_path=document_path)
        # assert
        assert not client._http_client.is_closed  # noqa: SLF001

    # httpx client is closed when exiting the context manager
    assert client._http_client.is_closed  # noqa: SLF001

    # Ensure entering after closing works
    async with client:
        await client.get_result(document_path=document_path)
        # assert
        assert not client._http_client.is_closed  # noqa: SLF001


async def test_get_result_wait_for_cancelled_error(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    # arrange
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))

    async with client:
        get_result_task = asyncio.create_task(client.get_result(document_path=document_path))
        await asyncio.sleep(0.10)
        # act

    # assert
    with pytest.raises(WaitForResultCancelledError, match="Wait for result cancelled for document"):
        await get_result_task


async def test_get_result_cancel(
    ctx: Context,
    client: Client,
    document_path: Path,
    httpx_mock: HTTPXMock,
) -> None:
    httpx_mock.add_response(**response_upload(ctx=ctx))
    httpx_mock.add_response(**response_state(ctx=ctx, state=DocumentState.QUEUED_FOR_PROCESSING))

    async with client:
        get_result_task = asyncio.create_task(client.get_result(document_path=document_path))
        await asyncio.sleep(0.10)

        get_result_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await get_result_task


# TODO: low prio  # noqa: FIX002
# - file handling
#   - file not exists
#   - unsupported file (upload error)
# - support bytes for upload
