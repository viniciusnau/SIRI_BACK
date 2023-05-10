# SIRI

SIRI is a Django-based project developed for DPESC, aimed at efficiently managing internal processes within the organization.

## Installation
Install the package manager [pip](https://pip.pypa.io/en/stable/)

Install [docker](https://docs.docker.com/) & [docker-compose](https://docs.docker.com/compose/).

Create a [virtualenv](https://virtualenv.pypa.io/en/latest/) and activate it.

```bash
sudo apt install virtualenv && virtualenv SIRI_ENV && source SIRI_ENV/bin/activate
```

Install [pre-commit](https://pre-commit.com/).

```bash
pip3 install pre-commit && pre-commit install
```

Install requirements.txt

```bash
pip3 install -r requirements.txt
```

Create a .env file at the root with the following content. (ask the project manager to fill the fields)

```.env
SECRET_KEY=
DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=
DB_PORT=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_BUCKET_NAME=
AWS_REGION_NAME=
AWS_EXPIRES_SECONDS=
DEFAULT_FILE_STORAGE=
RESTRICTED_DATES=
DEBUG=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

Run the server:
```bash
make run
```
Log into the server shell by running:
```bash
make server-shell
```
Create a superuser:
```bash
python3 manage.py createsuperuser
```
Finally, populate database tables (I recommend using Dbeaver or other similar tool).
## Workflow

Take the first card of the first column in trello.

Copy the card's description.

Open a shell on the project root and follow the instructions.

```bash
git checkout developer
git pull
```
Then control + shift + v into the terminal to create a new branch from developer with the card's name.

After completing the task, update Swagger and make sure to run:
```bash
make all
```
The above command will run the project linters and tests.

All tests must pass and all the linting problems must be solved.

Test coverage cannot drop below 99%.

Create a Pull Request pointing base to developer.

Move the task card to the "review" column.

## Swagger Documentation
To access documentation, follow these steps:

1. Ensure that the project is running and the API is accessible.
2. Click the button below to access the Swagger documentation and interact with the available APIs:
[![Swagger Documentation](https://img.shields.io/badge/Swagger-Documentation-blue.svg)](http://0.0.0.0:8000/swagger)
3. You will be presented with the Swagger UI, which lists all the available endpoints.
4. Explore the APIs by expanding the endpoints and clicking on them to view details such as request/response parameters, headers, and example payloads.
5. To test an endpoint, click on the "Try it out" button, enter the required input parameters, and click "Execute" to see the response.
6. Feel free to experiment with different inputs and explore the capabilities of the API.

## How To Run Server

```bash
make run
```

## How To Run Pytest

```bash
make test
```

## How To Lint Project

```bash
make lint
```
## How To Open Server Shell

```bash
make server-shell
```

## How To Open DB Shell

```bash
make db-shell
```
