install:
	poetry install

migrate:
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

lint:
	poetry run flake8 task_manager --exclude=migrations,task_manager/settings.py,admin.py

shell:
	poetry run python manage.py shell

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

dev:
	poetry run python manage.py runserver