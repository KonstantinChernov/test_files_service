import hashlib
import json

from flask import g, jsonify, current_app
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import abort

from db.pg_db import db
from models.users import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login: str, password: str):
    user = User.query.filter_by(login=login).first()
    if not user or not user.check_password(password):
        return False
    g.user = user
    return True


def get_hash(file):
    h = hashlib.sha256()
    h.update(file.read())
    file.seek(0)
    return h.hexdigest()


def json_abort(status_code, message):
    data = {
        'error': {
            'code': status_code,
            'message': message
        }
    }
    response = jsonify(data)
    response.status_code = status_code
    abort(response)


def upload_users_fixtures():
    with open('db/fixtures/users.json') as json_users:
        users_data = json.load(json_users)
        for user_data in users_data:
            login = user_data.get('login')
            password = user_data.get('password')
            if not login or not password:
                current_app.logger.warning(f'no login or no password for user object {users_data.index(user_data)}')
                continue

            if User.query.filter_by(login=login).first() is not None:
                current_app.logger.warning(f'user with login {login} already exists')
                continue
            user = User(login=login)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info('users upload finished')
