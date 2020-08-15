from rest_framework import views, permissions, serializers
from rest_framework.settings import api_settings

from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    NON_FIELD_ERRORS as DJANGO_NON_FIELD_ERRORS_KEY,
)


def get_validation_error_detail(exc):
    """
    Consolidate Django & DRF validation error details into a consistent
    structure.
    """
    detail = serializers.as_serializer_error(exc)
    try:
        django_non_field_errors = detail.pop(DJANGO_NON_FIELD_ERRORS_KEY)
    except KeyError:
        pass
    else:
        non_field_errors = detail.pop(api_settings.NON_FIELD_ERRORS_KEY, [])
        non_field_errors.extend(django_non_field_errors)
        detail[api_settings.NON_FIELD_ERRORS_KEY] = non_field_errors
    return detail


class CustomSerializer(serializers.Serializer):
    """
    Allow for field name mapping.
    """

    field_name_mapping = {
        # 'from_field_name': "to_field_name",
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        for from_field_name, to_field_name in self.field_name_mapping.items():
            try:
                attrs[to_field_name] = attrs.pop(from_field_name)
            except KeyError:
                continue
        return attrs


class CustomModelSerializer(serializers.ModelSerializer):
    """
    Keep field errors consistent by mapping Django Model field names to custom
    DRF Serializer field names
    """

    model_field_name_mapping = {
        # 'model_field_name': 'serializer_field_name'
    }

    def map_model_field_names_to_serializer_field_names(self, attrs):
        for model_field_name, serializer_field_name in self.model_field_name_mapping.items():
            try:
                attrs[serializer_field_name] = attrs.pop(model_field_name)
            except KeyError:
                continue

    def map_serializer_field_names_to_model_field_names(self, attrs):
        for model_field_name, serializer_field_name in self.model_field_name_mapping.items():
            try:
                attrs[model_field_name] = attrs.pop(serializer_field_name)
            except KeyError:
                continue

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.map_serializer_field_names_to_model_field_names(attrs)
        return attrs

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except DjangoValidationError as e:
            error_dict = getattr(e, 'error_dict', {})
            if not error_dict:
                raise e
            self.map_model_field_names_to_serializer_field_names(error_dict)
            raise DjangoValidationError(error_dict)
        else:
            return instance

    def update(self, instance, validated_data):
        try:
            instance = super().update(instance, validated_data)
        except DjangoValidationError as e:
            error_dict = getattr(e, 'error_dict', {})
            if not error_dict:
                raise e
            self.map_model_field_names_to_serializer_field_names(error_dict)
            raise DjangoValidationError(error_dict)
        else:
            return instance


class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


def custom_exception_handler(exc, context):
    # Ensure both Django & DRF validation errors are displayed in a consistent
    # way.
    try:
        detail = get_validation_error_detail(exc)
        exc = serializers.ValidationError(detail)
    except AssertionError:
        pass

    # Call DRF's default exception handler to get the standard error response.
    response = views.exception_handler(exc, context)

    return response
