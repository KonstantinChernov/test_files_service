import os
from http import HTTPStatus

from flask import Blueprint, g, request, send_from_directory

from models.files import File
from services.files_handlers import FileDeleter, FileSaver
from services.utils import auth, json_abort

files = Blueprint('files', __name__)


@files.route('/upload', methods=['POST'])
@auth.login_required()
def upload_file():
    if uploaded_file := request.files.get('file', None):
        return FileSaver(file=uploaded_file, user_id=g.user.id).run()
    json_abort(HTTPStatus.BAD_REQUEST, "file not found")


@files.route('/download/<filename>', methods=['GET'])
def download(filename: str):
    if file := File.query.filter_by(filename=filename).first():
        return send_from_directory(os.path.dirname(file.path), file.filename, as_attachment=True)
    json_abort(HTTPStatus.NOT_FOUND, "file not found")


@files.route('/delete/<filename>', methods=['DELETE'])
@auth.login_required()
def delete(filename: str):
    return FileDeleter(filename=filename, user_id=g.user.id).run()
