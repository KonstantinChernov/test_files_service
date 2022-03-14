import os
import pathlib
import uuid
from http import HTTPStatus
from typing import Optional

from flask import current_app, jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.datastructures import FileStorage

from db.pg_db import db
from models.files import File
from services.utils import get_hash, json_abort


class FileSaver:
    def __init__(self, file: FileStorage, user_id: uuid.UUID):
        self.file: FileStorage = file
        self.user_id: uuid.UUID = user_id
        self.filename: Optional[str] = None
        self.folder_of_file: Optional[pathlib.Path] = None
        self.full_path_of_file: Optional[pathlib.Path] = None

    def get_hashed_filename(self):
        self.filename = get_hash(self.file)

    def create_folder_in_storage(self):
        self.folder_of_file = os.path.join(current_app.config['UPLOAD_PATH'], self.filename[:2])
        self.full_path_of_file = os.path.join(self.folder_of_file, self.filename)

        if os.path.exists(self.full_path_of_file):
            json_abort(HTTPStatus.BAD_REQUEST, "such file already exists")

        if not os.path.exists(self.folder_of_file):
            os.makedirs(self.folder_of_file)

    def save_to_storage(self):
        try:
            self.file.save(os.path.join(self.folder_of_file, self.filename))
        except Exception as e:
            current_app.logger.error(e)
            json_abort(HTTPStatus.INTERNAL_SERVER_ERROR, "something went wrong. please try later")

    def add_entity_to_db(self):
        obj = File(filename=self.filename, path=self.full_path_of_file, user_id=self.user_id)
        db.session.add(obj)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(e)
            json_abort(HTTPStatus.INTERNAL_SERVER_ERROR, "something went wrong. please try later")

    def run(self):
        self.get_hashed_filename()
        self.create_folder_in_storage()
        self.save_to_storage()
        self.add_entity_to_db()
        return jsonify({"saving": self.filename}), HTTPStatus.CREATED


class FileDeleter:
    def __init__(self, filename: str, user_id: uuid.UUID):
        self.filename: str = filename
        self.user_id: uuid.UUID = user_id
        self.file: Optional[File] = None

    def check_file(self):
        self.file = File.query.filter_by(filename=self.filename).first()
        if not self.file:
            json_abort(HTTPStatus.NOT_FOUND, "such file does not exist")

        if self.file.user_id != self.user_id:
            json_abort(HTTPStatus.FORBIDDEN, "not enough permissions")

    def remove_from_storage(self):
        try:
            os.remove(self.file.path)
            if not os.listdir(os.path.dirname(self.file.path)):
                os.rmdir(os.path.dirname(self.file.path))
        except Exception as e:
            current_app.logger.error(e)
            json_abort(HTTPStatus.INTERNAL_SERVER_ERROR, "something went wrong. please try later")

    def remove_entity_from_db(self):
        db.session.delete(self.file)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(e)
            json_abort(HTTPStatus.INTERNAL_SERVER_ERROR, "something went wrong. please try later")

    def run(self):
        self.check_file()
        self.remove_from_storage()
        self.remove_entity_from_db()
        return jsonify({"deleted": self.filename}), HTTPStatus.NO_CONTENT
