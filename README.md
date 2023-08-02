<div align="center" style="padding-bottom: 10px">
    <h1>DoNotExpire</h1>
    <img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
    <img alt="Django" src="https://img.shields.io/badge/django%20-%23092E20.svg?&style=for-the-badge&logo=django&logoColor=white"/>
    <img alt="HTML" src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
    <img alt="CSS" src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
    <img alt="JavaScript" src="https://img.shields.io/badge/javascript%20-%23323330.svg?&style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Railway-%23000000.svg?&style=for-the-badge&logo=railway&logoColor=white" alt=""/>
</div>

<div align="center">
    <p>DoNotExpire is a website that makes keeping your Diablo 2 accounts safe from expiring much easier.</p>
    <p>Built with Django framework, HTML, CSS, vanilla Javascript and a bit of JQuery.</p>
</div>

# Overview:

Multiplayer Diablo II characters expire if they are inactive for too long. Expired characters cannot be recovered.
Single Player characters do not expire.

**Newly created characters will expire after 10 days of inactivity. Characters played for two hours or more will expire
after 90 days of inactivity.** To reset the inactivity timer on a character, you need to log in to an active game with
that character and buy or sell an item, or kill a monster.

Diablo II **accounts are also deleted after 90 days of inactivity.**

Thanks to DoNotExpire you can keep track of all your accounts. Log in and add your accounts, which hold up to 16
characters, to the database.  
Whenever you log into your Diablo 2 account, open the website and press the button next to the character you have just '
permed' ingame. The expiration date for this character will refresh on the website and you will be able to manually
follow those dates.  
Should you not perm your character and update the info on website, you will be sent an email with a notification to do
so.

If you keep forgetting to sync your Diablo 2 accounts state with website data, create a simple script to open both your
browser with this website and Diablo 2 game instance at the same time. This way you will most likely remember to update
the dates.

## Development Setup

### Without Docker

Create `.env` file with the following content:

```dotenv
SECRET_KEY=your_secret_key
```

Create virtual environment, activate it and install requirements with pipenv

```bash
mkdir .venv

pipenv shell

pipenv install
```

**or** with virtualenv

```bash
py -3 -m venv venv

venv\Scripts\Activate

pip install -r requirements.txt
```

Run migrations

```bash
python manage.py makemigrations

python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

Run unit tests and get code coverage

```bash
coverage run manage.py test

coverage report -m
```

### With Docker

Create `.env` file with the following content:

```dotenv
DJANGO_SETTINGS_MODULE=core.settings.dev

SECRET_KEY=...

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres

POSTGRES_DB=${DB_NAME}
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}
```

Make sure Docker Engine is running.

While in root directory, build docker images and run them with docker-compose. This might take up to few minutes.
Rebuilding image is crucial after installing new packages via pipenv.

Bringing up containers (with optional --build flag to rebuild images)

```shell
docker compose up --build
```

Bringing down containers with optional -v flag removes all attached volumes and invalidates caches.

```shell
docker compose down
```

Run commands inside docker, e.g.:

```shell
docker exec -it backend python manage.py makemigrations

docker exec -it backend python manage.py migrate

docker exec -it backend python manage.py createsuperuser
```

Application will be up at `127.0.0.1:8000`.

## Deployment to Railway

Go to https://railway.app/dashboard and create a new blank project.

Add Postgres database service.

Add backend service deployed from GitHub Repo.

Set environment variables in backend service:

```dotenv
RAILWAY_DOCKERFILE_PATH=Dockerfile.prod
PORT=8000
SECRET_KEY=...
PRODUCTION_HOST=<app_name>.up.railway.app
DJANGO_SETTINGS_MODULE=core.settings.prod
DATABASE_URL=${{<postgres_service_name>.DATABASE_URL}}
```

Add start command in deploy section:
```shell
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## Deployment to Heroku (Deprecated)

Set env variables in dashboard settings or with CLI

```dotenv
SECRET_KEY=...
PRODUCTION_HOST=<app_name>.herokuapp.com
DJANGO_SETTINGS_MODULE=core.settings.prod
```
