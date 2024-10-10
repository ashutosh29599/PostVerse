.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python3 manage.py migrate

.PHONY: migrations
migrations:
	poetry run python3 manage.py makemigrations

.PHONY: run-server
run-server:
	poetry run python3 manage.py runserver

.PHONY: superuser
superuser:
	poetry run python3 manage.py createsuperuser

.PHONY: update
update: install migrate ;

.PHONY: test
test:
	poetry run python3 manage.py test $(module)

.PHONY: show-urls
show-urls:
	poetry run python3 manage.py show_urls

.PHONY: shell
shell:
	 poetry run python3 manage.py shell
