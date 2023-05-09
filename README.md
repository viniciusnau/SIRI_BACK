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
RESTRICTED_DATES=
DEBUG=
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

After completing the task, make sure to run:
```bash
make all
```
The above command will run the project linters and tests.

All tests must pass and all the linting problems must be solved.

Test coverage cannot drop below 99%.

Create a Pull Request pointing base to developer.

Move the task card to the "review" column.
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
