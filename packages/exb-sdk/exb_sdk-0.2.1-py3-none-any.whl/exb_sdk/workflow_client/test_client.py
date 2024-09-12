from dataclasses import dataclass
from pathlib import Path
from typing import Self
from uuid import uuid4

from exb_sdk.workflow_client.client import Client, Result


class ResultNotFoundError(Exception):
    """Raised when a result is not found by the TestClient."""

    def __init__(self, document_path: Path) -> None:  # noqa: D107
        message = f"Missing result for '{document_path}'"
        super().__init__(message)


Results = dict[Path, Result]


@dataclass(kw_only=True)
class TestClient(Client):
    """A client that can be used when writing tests.

    >>> from exb_sdk.workflow_client import TestClient
    >>> workflow_client = TestClient.create(results={Path("mydoc.pdf"): {"documentId": "1234"}})
    >>> await my_processing_function(workflow_client=workflow_client)
    """

    # Prevent pytest from discovering this class
    __test__ = False

    results: Results

    @classmethod
    def create(cls, results: Results) -> Self:
        """Create a test client by configuring results.

        This should be the only method used for creating a TestClient.

        Args:
            results: A dictionary of document paths to their result.

        Returns:
            A new TestClient instance.
        """
        return cls(
            base_url="http://example.com",
            customer_id=uuid4(),
            solution_id=uuid4(),
            token="token",  # noqa: S106
            results=results,
        )

    async def get_result(self, document_path: Path) -> Result:
        """An overridden method for the test client not to make any external requests.

        Args:
            document_path: The path of the document to be uploaded and extracted.

        Raises:
            ResultNotFoundError: if the document_path is not part of the pre-configured results.

        Returns:
            The result of the pre-configured document as a dictionary.
        """
        try:
            return self.results[document_path]
        except KeyError:
            raise ResultNotFoundError(document_path=document_path) from None
