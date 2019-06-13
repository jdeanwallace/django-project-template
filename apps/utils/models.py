import json

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.forms.jsonb import (
    JSONField as JSONFormField, InvalidJSONInput,
)
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError


# Create your models here.
class CreatedModifiedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class UpdateModelMixin(object):

    def update(self, _force_save=False, **kwargs):
        modified = False
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value() if callable(value) else value)
                modified = True

        if modified or _force_save:
            self.save()


class JSONObjectFormField(JSONFormField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid JSON object."),
    }
    empty_values = [None, '', [], ()]

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            python_value = json.loads(value)
            if not isinstance(python_value, (dict,)):
                raise ValueError()
            return python_value
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            bound_data = json.loads(data)
            if not isinstance(bound_data, (dict,)):
                raise ValueError()
            return bound_data
        except ValueError:
            return InvalidJSONInput(data)


class JSONArrayFormField(JSONFormField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid JSON array."),
    }
    empty_values = [None, '', {}, ()]

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            python_value = json.loads(value)
            if not isinstance(python_value, (list,)):
                raise ValueError()
            return python_value
        except ValueError:
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            bound_data = json.loads(data)
            if not isinstance(bound_data, (list,)):
                raise ValueError()
            return bound_data
        except ValueError:
            return InvalidJSONInput(data)


class JSONObjectField(JSONField):
    description = _('A JSON object')
    default_error_messages = {
        'invalid': _("Value must be a valid JSON object."),
    }
    empty_values = [None, '', [], ()]

    def __init__(self, verbose_name=None, name=None, encoder=DjangoJSONEncoder,
                 **kwargs):
        super().__init__(verbose_name, name, encoder, **kwargs)

    def validate(self, value, model_instance):
        if not isinstance(value, (dict,)):
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        super().validate(value, model_instance)

    def formfield(self, **kwargs):
        defaults = {'form_class': JSONObjectFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class JSONArrayField(JSONField):
    description = _('A JSON array')
    default_error_messages = {
        'invalid': _("Value must be a valid JSON array."),
    }
    empty_values = [None, '', {}, ()]

    def __init__(self, verbose_name=None, name=None, encoder=DjangoJSONEncoder,
                 **kwargs):
        super().__init__(verbose_name, name, encoder, **kwargs)

    def validate(self, value, model_instance):
        if not isinstance(value, (list,)):
            raise ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        super().validate(value, model_instance)

    def formfield(self, **kwargs):
        defaults = {'form_class': JSONArrayFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
