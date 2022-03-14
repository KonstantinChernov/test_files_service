import hashlib

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import abort

from models.users import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login, password):
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
