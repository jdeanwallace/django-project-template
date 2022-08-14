<!-- {% if False %} -->

# Django Project Template

## Overview
Kickstart any new Django project with the following features already built-in:
- A custom `AUTH_USER_MODEL`:
  - No fields are required to create a new `User`.
  - The `username` field is an auto-generated UUID.
  - The `email` field is unique and optional.
  - `User`'s login using an `email` & `password` combination.
  - [DRF](https://www.django-rest-framework.org/) auth token integration.
- A neat `/apps` directory for all your Django apps.
- A `utils` app for all your commonly used functions & models, including:
  - A custom `JSONObjectField` & `JSONArrayField` to help enforce the integrity of your JSON data.
- A `/settings` directory for separate environment settings like dev & prod.
- Basic [Celery](https://docs.celeryproject.org/en/latest/index.html) config.
- Basic [logging](https://docs.python.org/3/library/logging.html) config.

## Requirements
- Python (3.5+)
- Django (3.1+)

## Usage
```bash
django-admin startproject \
  --template https://github.com/jdeanwallace/django-project-template/zipball/master \
  --extension py,md \
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
cd /path/to/project/directory
python -m venv venv
. venv/bin/activate
pip install -r requirements/dev.txt
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
...
./manage.py runserver
```

{{ "<!"|add:"--" }} End. -->
