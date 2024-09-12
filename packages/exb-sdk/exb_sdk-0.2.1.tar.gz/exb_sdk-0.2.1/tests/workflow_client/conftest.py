from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest

from exb_sdk.workflow_client import Result
from exb_sdk.workflow_client._api_constants import DocumentState


@pytest.fixture
def resources() -> Path:
    return Path(__file__).parent / "resources"


@pytest.fixture
def document_path(resources: Path) -> Path:
    return resources / "empty.png"


@dataclass
class Context:
    customer_id: UUID
    solution_id: UUID
    document_id: UUID
    base_url: str


Response = dict[str, Any]


@pytest.fixture
def ctx() -> Context:
    return Context(
        customer_id=uuid4(),
        solution_id=uuid4(),
        document_id=uuid4(),
        base_url="http://example.com",
    )


def response_upload(ctx: Context) -> Response:
    return {
        "url": f"http://example.com/{ctx.customer_id}/{ctx.solution_id}/latest/upload?keep_cache=false",
        "status_code": 202,
        "method": "POST",
        "json": f"{ctx.customer_id}/{ctx.solution_id}/latest/state/{ctx.document_id}",
    }


def response_state(
    ctx: Context,
    state: DocumentState,
) -> Response:
    return {
        "url": f"http://example.com/{ctx.customer_id}/{ctx.solution_id}/latest/state/{ctx.document_id}",
        "status_code": 200,
        "method": "GET",
        "json": {
            "id": str(ctx.document_id),
            "state": state.value,
            "stateUrl": f"{ctx.customer_id}/{ctx.solution_id}/latest/state/{ctx.document_id}",
            "resultUrl": (
                f"{ctx.customer_id}/{ctx.solution_id}/latest/result/{ctx.document_id}/main",
            ),
        },
    }


def response_result(ctx: Context, result: Result) -> Response:
    return {
        "url": f"http://example.com/{ctx.customer_id}/{ctx.solution_id}/latest/result/{ctx.document_id}/main",
        "status_code": 200,
        "method": "GET",
        "json": result,
    }
