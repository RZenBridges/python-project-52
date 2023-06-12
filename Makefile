migrate_db:
	poetry run python3 manage.py migrate

start:
	poetry run gunicorn -w 5 task_manager.wsgi:application

dev:
	poetry run python3 manage.py runserver

lint:
	poetry run python3 -m flake8 task_manager

install:
	poetry install
