import json

from core import create_app
from db.pg_db import db
from models.users import User

app = create_app()


@app.cli.command("add_users_from_fixtures")
def add_users_from_fixtures():
    with open('db/fixtures/users.json') as json_users:
        users_data = json.load(json_users)
        for user_data in users_data:
            login = user_data.get('login')
            password = user_data.get('password')
            if not login or not password:
                app.logger.warning(f'no login or no password for user object {users_data.index(user_data)}')
                continue

            if User.query.filter_by(login=login).first() is not None:
                app.logger.warning(f'user with login {login} already exists')
                continue
            user = User(login=login)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            app.logger.info('users upload finished')
