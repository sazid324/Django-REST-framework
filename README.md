# TolHub API and Backend Server

## Installation

### Using Docker Compose

```shell
docker compose up -d
```

### Local Installation

1. Create a virtual environment:

```shell
python -m venv env
```

2. Activate the environment:

   - Linux:

   ```shell
   source env/bin/activate
   ```

   - Windows:

   ```shell
   .\env\Scripts\activate
   ```

3. Install the requirements:

```shell
pip install --upgrade pip setuptools
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

4. Create a logs directory:

```shell
mkdir logs
```

## Starting the Server

- Linux:

```shell
python manage.py runserver
```

- Windows:

```shell
python manage.py runserver
```

# Developer Guide

1. Start by pulling the develop branch.
2. Create branches from the develop branch.
3. Delete branches after merging.

## Commit Convention

The commit follows the following structural elements to communicate intent to the consumers of your library:

- `fix`: a commit that patches a bug in your codebase (correlates with PATCH in Semantic Versioning).
- `feat`: a commit that introduces a new feature to the codebase (correlates with MINOR in Semantic Versioning).
- `BREAKING CHANGE`: a commit that introduces a breaking API change (correlates with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
  - Other types allowed: build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
  - Footers other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to git trailer format.
  - Additional types are not mandated by the Conventional Commits specification unless they include a BREAKING CHANGE.
  - A scope may be provided to a commit’s type, contained within parenthesis, to provide additional contextual information.

## Seeding Data

After migrating to a new database, you can run seed:

```shell
python manage.py loaddata seed/*.json
```

## Generating Seed on App

```shell
python manage.py seed app_name --number=100 --settings tolhub.settings_dev
```

## Creating New Seed

```shell
python manage.py dumpdata app_name --indent 4 > seed/file_name.json
```

Replace `app_name` with the Django app name and `file_name` with any name starting with a sequence like `0001`.

## Default Admin Credentials

- Email: admin@gmail.com
- Password: admin@123

## Default User Credentials

- Email: user@gmail.com
- Password: user@123
