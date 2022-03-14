import io

import pytest

from core import create_app
from db.pg_db import db
from models.users import User

FILE_BYTES = b'abcdefdvsef'


@pytest.fixture(scope='session')
def app():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        user1 = User(login='Admin')
        user1.set_password('123')
        user2 = User(login='Admin1')
        user2.set_password('123')
        db.session.add_all([user1, user2])
        db.session.commit()
        yield app
        db.session.rollback()
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def test_client(app):
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()
