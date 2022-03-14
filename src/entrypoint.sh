#!/bin/bash

exec gunicorn core.app:app -b 0.0.0.0:5000 --reload -w 4
