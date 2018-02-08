# Pathways backend

This repository contains the server for providing access to data about services for refugees and immigrants to BC.

At this stage, our focus is on establishing the server architecture and testing frameworks for unit, integration and feature testing, continuous integration, logging, etc. The domain model is still that from a django turorial on polls, with a single one-to-many relationship from questions to choices. The plan is for future services to be built with the polls service as pattern, and the polls patter to be discarded. This will happen as our understanding of our domain improves.

## Getting started

Clone the repository

```
git clone git@github.com:pg-irc/pathways-backend.git
```

Set up and activate a python v3 environment

```
cd pathways-backend/
python3 -m venv .venv
source .venv/bin/activate
```

Install the required python libraries for local development

```
pip install -r requirements/local.txt
```

Create the database tables. For local development, sqlite is the database implementation, for production, postgres is used.

```
python manage.py migrate
```

Create the django administration account:

```
python manage.py createsuperuser
```

Run the unit tests

```
python manage.py test
```

Start the API server

```
python manage.py runserver
```

You should now be able to access the server at http://127.0.0.1:8000/v1/. The Django admin tool is at http://127.0.0.1:8000/v1/admin/, and the question and choice entities are available at http://127.0.0.1:8000/v1/questions/ and http://127.0.0.1:8000/v1/questions/1/choices/.

Import BC-211 data

```
python manage.py import_bc211_data ~/path/to/AIRSXML_2252_Export_20170109050136__211.xml

```

## Using different settings

By default the local settings are used. To use other settings, use the environment variable `DJANGO_SETTINGS_MODULE`, valid values are `config.settings.local`, `config.settings.test` and `config.settings.production`.

## Running tests on Travis and locally

Travis runs the tests using the settings in `config.settings.test`, against postgres using the accont "postgres" with empty password, creating a database called "test_db". To run the same tests locally, create a postgres user and a database called "test_db" owned by that user, and specify the postgres account using environment variables `POSTGRES_USER` and `POSTGRES_PASSWORD`, either on the command line:

```
DJANGO_SETTINGS_MODULE=config.settings.test POSTGRES_USER=test_user POSTGRES_PASSWORD='the_password' python manage.py test
```

or put these settings in a file called .env (use env.example as a template) and `export DJANGO_READ_DOT_ENV_FILE=True` to make sure the file is read.

## Upgrading packages

There is a utility script that may be used to update the python packages. Before using it, it may be a good idea to make sure that you have a correct environment based off of the requirements for the _local_ environment.

```
deactivate
rm -r .venv-local/
python3 -m venv .venv-local
source ./.venv-local/bin/activate
pip install -r requirements/local.txt
```

Then run the upgrade script for either local, rest or production environment, e.g.:

```
./utility/upgrade_packages.sh production
```

You will be prompted to decide which of the possible upgrades you will take (this is using [pur](https://pypi.python.org/pypi/pur) in interactive mode), the requirement files are updated and a new environment is created using the new packages for use in testing before the upgrades are committed.

## Getting started with Heroku

Create a Heroku instance with these environment variables:

* DATABASE_URL (managed by Heroku)
* DJANGO_AWS_STORAGE_BUCKET_NAME=peacegeeks-pathways-static
* DJANGO_SECRET_KEY
* DJANGO_SETTINGS_MODULE=config.settings.production

Update ALLOWED_HOSTS production settings to include the name of the heroku instance

To clear out the database content

```
% heroku restart
% heroku pg:reset DATABASE
```

To initialize the database schema

```
% heroku run ./manage.py migrate
```

To connect to the heroku instance over SSH:

```
heroku ps:exec
```

To retrieve and import the BC-211 dataset:

```
wget https://s3.ca-central-1.amazonaws.com/peacegeeks-pathways-static/bc211data.xml

export DJANGO_SETTINGS_MODULE=config.settings.production
export DJANGO_SECRET_KEY="the key"
export DJANGO_AWS_STORAGE_BUCKET_NAME=peacegeeks-pathways-static
export DJANGO_MAILGUN_API_KEY="the key"
export MAILGUN_SENDER_DOMAIN="the domain"
export DATABASE_URL="the database url from heroku settings"

./manage.py import_bc211_data bc211data.xml

```

## Getting started with docker

Create and launch the docker containers for local development

```
docker-compose -f compose-local.yml build
```

Set up the database inside the container

```
docker-compose -f compose-local.yml run django python manage.py migrate
docker-compose -f compose-local.yml run django python manage.py createsuperuser
```

Launch the container

```
docker-compose -f compose-local.yml up
```

and check out http://localhost:8000/ to see if it worked. See https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html for more details.

## Translations

Certain content is translatable, using [django-parler](http://django-parler.readthedocs.io/). The *translation* module provides management commands to export translatable strings as POT files, and import their translations from PO files.

List available translatable models:

    ./manage.py content_translation_list_models

Create a POT file for a particular translatable model:

    ./manage.py content_translation_export organizations.organization > organization.pot

Or create a PO file with a model's current French translations:

    ./manage.py content_translation_export organizations.organization --language=fr > fr/organization.po

The resulting files can be edited in an application such as [GTranslator](https://wiki.gnome.org/Apps/Gtranslator) or [Poedit](https://poedit.net/).

After a translation file has been modified, you can import it again:

    ./manage.py content_translation_import fr/organization.po

## Development

### Null and django blank

Required string fields should never be null and never be the empty string. Optional string fields should never be the empty string. To achieve this, `blank` parameters to field definitions should always be the same as the `null` parameter, e.g. either `null=True, blank=True` or `null=False, blank=False`, the latter being the default values for both fields, which can therefore be omitted.

### Commit messages

All commits are labelled with the issue they are being done under. This ensures that we don't do work that is not tracked, and history of why every change is made is maintained. Most front end and back end work is tracked by issues in their respective repositories, in which case the commit message should start with "Issue #N", e.g. "Issue #13". Occasionally, front end work may be tracked under backend issues, in which case each commits message should start with "Issue pg-irc/pathways-backend#13".
