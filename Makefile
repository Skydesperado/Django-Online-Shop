.PHONY: runserver
runserver:
	pipenv run python manage.py runserver

.PHONY: check
check:
	pipenv run python manage.py check

.PHONY: migrations
migrations:
	pipenv run python manage.py makemigrations

.PHONY: migrate
migrate:
	pipenv run python manage.py migrate

.PHONY: superuser
superuser:
	pipenv run python manage.py createsuperuser

.PHONY: install-precommit
install-precommit:
	pipenv run pre-commit uninstall; pipenv run pre-commit install

.PHONY: lint
lint:
	pipenv run pre-commit run --all-files
