<!-- {% if False %} -->

# Django Project Template
---

## Usage
```bash
django-admin.py startproject \
  --template https://github.com/jdeanwallace/django-project-template/zipball/master \
  --extension py,md \
  PROJECT_NAME [/path/to/project/directory]
```

<!-- {% endif %}Hello, World! -->

# {{ project_name|title }} Django Project
---

## Features
- Custom `AUTH_USER_MODEL`.
  - No fields are required to create a new `User`.
  - The username field is an auto-generated uuid.
  - The email field is unique and optional.
  - `User`'s login using an `email` & `password` combination.
- A neat `/apps` directory for all your Django apps.
- A `utils` app for all your commonly used functions & models.

---
**Disclaimer**: *This was made just for me. This is what I use for all my new
Django projects. Who knows, maybe you can use it too. Please enjoy!*
