import io

import pytest

from services.utils import get_hash
from tests.functional.conftest import FILE_BYTES


@pytest.mark.run(order=3)
def test_download(test_client):
    response = test_client.get(
        f"/api/v1/files/download/{get_hash(io.BytesIO(FILE_BYTES))}",
    )
    assert response.data == FILE_BYTES
    assert response.status_code == 200


def test_not_download_not_existing_file(test_client):
    response = test_client.get(
        "/api/v1/files/download/not-existing-file",
    )
    assert response.status_code == 404
