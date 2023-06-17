test:
	poetry run python3 manage.py test

rallback_db:
	poetry run python3 manage.py migrate task zero
	poetry run python3 manage.py migrate status zero
	poetry run python3 manage.py migrate user zero
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

migrate_db:
	poetry run python3 manage.py makemigrations
	poetry run python3 manage.py migrate

start:
	poetry run python3 manage.py migrate
	poetry run gunicorn -w 5 task_manager.wsgi:application

dev:
	poetry run python3 manage.py runserver

lint:
	poetry run python3 -m flake8 task_manager

install:
	poetry install
