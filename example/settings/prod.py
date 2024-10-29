from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "example.fly.dev",
    "example.com",
]

EMAIL_BACKEND = "django_ses.SESBackend"

AWS_SES_ACCESS_KEY_ID = os.environ.get("AWS_SES_ACCESS_KEY_ID", "")
AWS_SES_SECRET_ACCESS_KEY = os.environ.get("AWS_SES_SECRET_ACCESS_KEY", "")
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", "")
AWS_SES_REGION_ENDPOINT = os.environ.get("AWS_SES_REGION_ENDPOINT", "")

SERVER_EMAIL = "Example Server <server@example.com>"
DEFAULT_FROM_EMAIL = "Admin from Example <admin@example.com>"
ADMINS = [("Admin", "admin@example.com")]
