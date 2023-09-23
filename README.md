<!-- Source: https://github.com/jdeanwallace/django-project-template -->

<!-- Start -->

# Example Django Project
---

## Getting Started

```bash
cd /path/to/project/directory
python -m venv venv
. venv/bin/activate
pip install pip-tools --upgrade
pip-sync requirements/dev.txt
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
...
./manage.py runserver
```

<!-- End. -->
