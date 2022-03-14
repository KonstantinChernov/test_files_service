#!/bin/bash

flask db upgrade
flask add_users_from_fixtures
exec gunicorn core.app:app -b 0.0.0.0:5000 --reload -w 4
