run:
	docker-compose up

server-up:
	docker start SIRI_SERVER

server-down:
	docker stop SIRI_SERVER

db-up:
	docker start SIRI_DATABASE

db-down:
	docker stop SIRI_DATABASE

server-shell:
	docker exec -it SIRI_SERVER /bin/bash

db-shell:
	docker exec -it SIRI_DATABASE /bin/bash

test: db-up server-up
	docker exec -it SIRI_SERVER pytest --cov-fail-under=99
	docker stop SIRI_SERVER
	docker stop SIRI_DATABASE

lint:
	docker exec -it SIRI_SERVER isort .
	docker exec -it SIRI_SERVER black .
	docker exec -it SIRI_SERVER flake8 --exit-zero

all: test lint