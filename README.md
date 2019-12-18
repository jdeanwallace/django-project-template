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
- A `utils` app for all your commonly used functions & models.
- A `/settings` directory for separate environment settings like dev & prod.
- Basic [Celery](https://docs.celeryproject.org/en/latest/index.html) config.
- Basic [logging](https://docs.python.org/3/library/logging.html) config.

## Requirements
- Python (3.5+)
- Django (1.11+)

## Usage
```bash
django-admin.py startproject \
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
mkvirtualenv {{ project_name }}
cd /path/to/project/directory
pip install -r requirements/dev.txt
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
...
./manage.py runserver
```

{{ "<!"|add:"--" }} End. -->
