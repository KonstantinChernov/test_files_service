from core import create_app
from db.pg_db import db
from services.utils import upload_users_fixtures

app = create_app()


@app.cli.command("add_users_from_fixtures")
def add_users_from_fixtures():
    upload_users_fixtures()


@app.before_first_request
def setup_db():
    db.create_all()
    upload_users_fixtures()


@app.teardown_appcontext
def close_db(sender, **extra):
    db.session.close()
