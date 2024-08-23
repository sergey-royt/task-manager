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
	poetry run flake8 task_manager --exclude=migrations,settings.py,admin.py

shell:
	poetry run python manage.py shell