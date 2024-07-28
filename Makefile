install:
	poetry install

migrate:
	poetry run python manage.py migrate

test:
	poetry run python manage.py test

lint:
	poetry run flake8 task_manager --exclude=migrations,settings.py,admin.py,models.py

shell:
	poetry run python manage.py shell