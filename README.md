<!-- Source: https://github.com/jdeanwallace/django-project-template -->

<!-- Start -->

# Example Django Project
---

## Getting Started

```bash
python -m venv venv && \
  . venv/bin/activate && \
  pip install pip-tools --upgrade && \
  pip-sync requirements/dev.txt && \
  python manage.py makemigrations && \
  python manage.py migrate && \
  python manage.py createsuperuser

python manage.py runserver
```

<!-- End. -->
