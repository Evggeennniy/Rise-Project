SHELL := /bin/bash

manage_py := python3 app/manage.py
# ^ Using variables to determine repeated references

run1:
	$(manage_py) runserver 127.0.0.1:8000

createsuperuser:
	$(manage_py) createsuperuser

newmig:
	$(manage_py) makemigrations

mig:
	$(manage_py) migrate

shellplus:
	$(manage_py) shell_plus --print-sql

pytest:
	pytest app/tests/

covtest:
	pytest --cov=app app/tests/ --cov-report html && coverage report --fail-under=80

showcovtest:
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"

server1:
	cd app && gunicorn settings.wsgi:application --bind 0.0.0.0:8001 --workers 2 --threads 2 --log-level info --max-requests 20 --timeout 10

server2:
	cd app && gunicorn settings.wsgi:application --bind 0.0.0.0:8002 --workers 5 --threads 2 --log-level info --max-requests 20 --timeout 10

setup:
	pip install -r requirements.txt

collstat:
	$(manage_py) collectstatic

runcelw:
	cd app & celery -A settings worker --loglevel=INFO

runcelb:
	cd app & celery -A settings beat --loglevel=INFO

build_and_run:
	$(manage_py) makemigrations 
	$(manage_py) migrate 
	$(manage_py) runserver
