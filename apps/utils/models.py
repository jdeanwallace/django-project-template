import json

from django import forms
from django.db import models
from django.core import exceptions
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CreatedModifiedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.modified_at = self.created_at
        else:
            self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class JSONFormField(forms.JSONField):

    def __init__(self, empty_value=None, **kwargs):
        super().__init__(**{"empty_value": None, **kwargs})

    def is_valid(self, value):
        return isinstance(value, (list, dict, int, float, forms.JSONString))

    def to_python(self, value):
        if self.disabled:
            return value
        try:
            # Try load JSON from string
            converted = json.loads(value, cls=self.decoder)
            if isinstance(converted, str):
                converted = forms.JSONString(converted)
        except json.JSONDecodeError:
            # Invalid JSON
            converted = forms.fields.InvalidJSONInput(value)
        except TypeError:
            # Not a string
            converted = value
        if converted in self.empty_values:
            return self.empty_value
        elif self.is_valid(converted):
            return converted
        raise exceptions.ValidationError(
            self.error_messages["invalid"],
            code="invalid",
            params={"value": value},
        )

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            # Try load JSON from string
            value = json.loads(data, cls=self.decoder)
            if not self.is_valid(value):
                raise ValueError(value)
        except (json.JSONDecodeError, ValueError):
            return forms.fields.InvalidJSONInput(data)
        else:
            return value


class JSONObjectFormField(JSONFormField):
    default_error_messages = {
        "invalid": _("'%(value)s' value must be a valid JSON object."),
    }
    empty_values = [None, ""]

    def is_valid(self, value):
        return isinstance(value, (dict,))


class JSONArrayFormField(JSONFormField):
    default_error_messages = {
        "invalid": _("'%(value)s' value must be a valid JSON array."),
    }
    empty_values = [None, ""]

    def is_valid(self, value):
        return isinstance(value, (list,))


class JSONObjectField(models.JSONField):
    description = _("A JSON object")
    default_error_messages = {
        "invalid": _("Value must be a valid JSON object."),
    }
    empty_values = [None, ""]

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value is not None and not isinstance(value, (dict,)):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": JSONObjectFormField,
                "required": not self.blank or not self.null,
                **kwargs,
            }
        )


class JSONArrayField(models.JSONField):
    description = _("A JSON array")
    default_error_messages = {
        "invalid": _("Value must be a valid JSON array."),
    }
    empty_values = [None, ""]

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value is not None and not isinstance(value, (list,)):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": JSONArrayFormField,
                "required": not self.blank or not self.null,
                **kwargs,
            }
        )
