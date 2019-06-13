from rest_framework import mixins, status, views, permissions, serializers
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.parsers import BaseParser
from rest_framework.renderers import BaseRenderer

from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    NON_FIELD_ERRORS as DJANGO_NON_FIELD_ERRORS_KEY,
)


def get_validation_error_detail(exc):
    """
    Convert Django's ValidationError into DRF's ValidationError detail style
    """
    assert isinstance(exc, DjangoValidationError), (
        "Can only extract detail from Django's ValidationError class."
    )
    try:
        error_dict = exc.error_dict
    except AttributeError:
        try:
            error_list = exc.error_list
        except AttributeError:
            return {
                api_settings.NON_FIELD_ERRORS_KEY: [exc.message % (exc.params or ())]
            }
        return {
            api_settings.NON_FIELD_ERRORS_KEY: [
                error.message % (error.params or ())
                for error in exc.error_list
            ]
        }
    return {
        (api_settings.NON_FIELD_ERRORS_KEY if k == DJANGO_NON_FIELD_ERRORS_KEY else k): [error.message % (error.params or ()) for error in error_list]
        for k, error_list in error_dict.items()
    }


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
            if model_field_name in attrs:
                attrs[serializer_field_name] = attrs.pop(model_field_name)

    def map_serializer_field_names_to_model_field_names(self, attrs):
        for model_field_name, serializer_field_name in self.model_field_name_mapping.items():
            if serializer_field_name in attrs:
                attrs[model_field_name] = attrs.pop(serializer_field_name)

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


class CustomCreateModelMixin(mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_serializer = self.serializer_class(
            instance=serializer.instance, context=self.get_serializer_context(),
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED,
            headers=headers,
        )


class CustomUpdateModelMixin(mixins.UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            self.serializer_class(instance=serializer.instance).data,
        )


def custom_exception_handler(exc, context):
    # Convert Django ValidationError's into DRF ValidationError's
    if isinstance(exc, (DjangoValidationError,)):
        exc = serializers.ValidationError(get_validation_error_detail(exc))

    # Call REST framework's default exception handler to get the standard
    # error response.
    response = views.exception_handler(exc, context)

    return response
