import os
from http import HTTPStatus

from flask import Blueprint, g, jsonify, request, send_from_directory

from models.files import File
from services.files_handlers import FileDeleter, FileSaver
from services.utils import auth

files = Blueprint('files', __name__)


@files.route('/upload', methods=['POST'])
@auth.login_required()
def upload_file():
    uploaded_file = request.files['file']
    return FileSaver(file=uploaded_file, user_id=g.user.id).run()


@files.route('/download/<filename>', methods=['GET'])
def download(filename: str):
    if file := File.query.filter_by(filename=filename).first():
        return send_from_directory(os.path.dirname(file.path), file.filename, as_attachment=True)
    return jsonify({"error": "file not found"}), HTTPStatus.NOT_FOUND


@files.route('/delete/<filename>', methods=['DELETE'])
@auth.login_required()
def delete(filename: str):
    return FileDeleter(filename=filename, user_id=g.user.id).run()
