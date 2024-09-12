from __future__ import annotations

from pathlib import Path

import pytest

from exb_sdk.workflow_client.test_client import ResultNotFoundError, TestClient


async def test_get_result(document_path: Path) -> None:
    # arrange
    client = TestClient.create(results={document_path: {"documentId": 1}})

    # act
    result = await client.get_result(document_path=document_path)

    # assert
    assert result == {"documentId": 1}


async def test_get_result_not_found(document_path: Path) -> None:
    # arrange
    client = TestClient.create(results={document_path: {"documentId": 1}})

    # assert
    with pytest.raises(ResultNotFoundError, match="Missing result for 'another-document.pdf'"):
        # act
        await client.get_result(document_path=Path("another-document.pdf"))
