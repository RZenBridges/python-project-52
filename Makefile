start:
	poetry run python3 task_manager/manage.py runserver

lint:
	poetry run python3 -m flake8 task_manager
