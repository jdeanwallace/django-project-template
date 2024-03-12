from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "{{ project_name }}.fly.dev",
    "{{ project_name }}.com",
]

EMAIL_BACKEND = "django_ses.SESBackend"

AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID", "")
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY", "")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", "")
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT", "")

SERVER_EMAIL = "{{ project_name|title }} Server <server@{{ project_name }}.com>"
DEFAULT_FROM_EMAIL = "Admin from {{ project_name|title }} <admin@{{ project_name }}.com>"
ADMINS = [("Admin", "admin@{{ project_name }}.com")]
