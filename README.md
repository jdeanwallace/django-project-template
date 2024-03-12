<!-- {% if False %} -->

# Django Project Template

## Overview
Kickstart any new Django project with the following features already built-in:
- A custom `AUTH_USER_MODEL`:
  - No fields are required to create a new `User`.
  - The `username` field is an auto-generated UUID.
  - The `email` field is unique and optional.
  - `User`'s login using an `email` & `password` combination.
- A neat `/apps` directory for all your Django apps.
- A `utils` app for all your commonly used functions & models, including:
  - A custom `JSONObjectField` & `JSONArrayField` to help enforce the integrity of your JSON data.
- A `/settings` directory for separate environment settings like dev & prod.
- Basic [Celery](https://docs.celeryproject.org/en/latest/index.html) config.
- Basic [logging](https://docs.python.org/3/library/logging.html) config.

## Requirements
- Python (3.9+)

## Usage
```bash
django-admin startproject \
  --template https://github.com/jdeanwallace/django-project-template/zipball/master \
  --extension py,md,toml \
  --name Dockerfile,package.json,package-lock.json \
  PROJECT_NAME [/path/to/project/directory]
```

---

**Note**: *This template helps me to get up & running with my new Django projects. Who knows, maybe it can help you too. Enjoy!*

<!-- {% endif %}Source: https://github.com/jdeanwallace/django-project-template -->

<!-- Start {{ "--"|add:">" }}

# {{ project_name|title }} Django Project
---

## Getting Started

```bash
python -m venv venv && \
  . venv/bin/activate && \
  pip install pip pip-tools --upgrade && \
  pip-sync requirements/dev.txt && \
  npm install && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py createsuperuser
```

## Run development server

```bash
npm run dev
```

## Deploy

### Launch fly.io app

```bash
fly launch --ha=false --volume-initial-size=1
```

### Set fly.io secrets

```bash
cat .env.prod | xargs fly secrets set
```

### Build bundles

```bash
npm run build
```

### Deploy changes when needed

```bash
fly deploy
```

{{ "<!"|add:"--" }} End. -->
