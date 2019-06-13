import uuid

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_uuid4(value):
    """
    Validate that a UUID string is in uuid4 format.
    """
    try:
        uuid.UUID(value, version=4)
    except (AttributeError, ValueError):
        raise ValidationError(
            _("'%(value)s' is not a valid UUID."),
            params={'value': value},
            code='invalid',
        )
