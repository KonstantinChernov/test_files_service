import base64
import io
import os

import pytest

from services.utils import get_hash
from tests.functional.conftest import FILE_BYTES


def test_not_upload_unregistered(test_client):
    response = test_client.post(
        "/api/v1/files/upload",
        data={'file': (io.BytesIO(FILE_BYTES), 'test.jpg')},
        content_type='multipart/form-data'
    )
    assert response.status_code == 401


@pytest.mark.run(order=1)
def test_upload(test_client, app):
    valid_credentials = base64.b64encode(b"Admin:123").decode("utf-8")
    response = test_client.post(
        "/api/v1/files/upload",
        data={'file': (io.BytesIO(FILE_BYTES), 'test.jpg')},
        headers={"Authorization": "Basic " + valid_credentials},
        content_type='multipart/form-data'
    )
    folder_of_file = os.path.join(app.config['UPLOAD_PATH'], get_hash(io.BytesIO(FILE_BYTES))[:2])
    full_path_of_file = os.path.join(folder_of_file, get_hash(io.BytesIO(FILE_BYTES)))
    assert os.path.exists(full_path_of_file)
    assert response.json['saving'] == get_hash(io.BytesIO(FILE_BYTES))
    assert response.status_code == 201


@pytest.mark.run(order=2)
def test_upload_second_time(test_client):
    valid_credentials = base64.b64encode(b"Admin:123").decode("utf-8")
    response = test_client.post(
        "/api/v1/files/upload",
        data={'file': (io.BytesIO(FILE_BYTES), 'test.jpg')},
        headers={"Authorization": "Basic " + valid_credentials},
        content_type='multipart/form-data'
    )
    assert response.json['error']['message'] == "such file already exists"
    assert response.status_code == 400
