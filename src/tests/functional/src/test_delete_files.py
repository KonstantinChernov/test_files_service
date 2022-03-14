import base64
import io
import os

import pytest

from services.utils import get_hash
from tests.functional.conftest import FILE_BYTES


@pytest.mark.run(order=4)
def test_not_delete_strangers_file(test_client):
    valid_credentials = base64.b64encode(b"Admin1:123").decode("utf-8")
    response = test_client.delete(
        f"/api/v1/files/delete/{get_hash(io.BytesIO(FILE_BYTES))}",
        headers={"Authorization": "Basic " + valid_credentials},
    )
    assert response.json["error"]["message"] == "not enough permissions"
    assert response.status_code == 403


@pytest.mark.run(order=5)
def test_delete(test_client, app):
    valid_credentials = base64.b64encode(b"Admin:123").decode("utf-8")
    response = test_client.delete(
        f"/api/v1/files/delete/{get_hash(io.BytesIO(FILE_BYTES))}",
        headers={"Authorization": "Basic " + valid_credentials},
    )
    assert response.status_code == 204
    folder_of_file = os.path.join(app.config['UPLOAD_PATH'], get_hash(io.BytesIO(FILE_BYTES))[:2])
    full_path_of_file = os.path.join(folder_of_file, get_hash(io.BytesIO(FILE_BYTES)))
    assert not os.path.exists(full_path_of_file)


@pytest.mark.run(order=5)
def test_not_delete_deleted(test_client):
    valid_credentials = base64.b64encode(b"Admin:123").decode("utf-8")
    response = test_client.delete(
        f"/api/v1/files/delete/{get_hash(io.BytesIO(FILE_BYTES))}",
        headers={"Authorization": "Basic " + valid_credentials},
    )
    assert response.json["error"]["message"] == "such file does not exist"
    assert response.status_code == 404
