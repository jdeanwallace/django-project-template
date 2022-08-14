from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings

from django.test import TestCase
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    NON_FIELD_ERRORS as DJANGO_NON_FIELD_ERRORS_KEY,
)
from django.db import models

from apps.utils.rest_framework import (
    get_validation_error_detail, CustomModelSerializer, CustomSerializer,
    custom_exception_handler,
)


class ValidationErrorDetailTest(TestCase):

    def test_unsupported_error(self):
        with self.assertRaises(AssertionError):
            detail = get_validation_error_detail(
                Exception("This is an error.")
            )

    def test_django_single_error(self):
        error = "This is an error."
        detail = get_validation_error_detail(
            DjangoValidationError(error)
        )
        self.assertEqual(
            detail,
            {
                "non_field_errors": [
                    "This is an error."
                ]
            }
        )

    def test_django_list_error(self):
        error = ["This is an error.", "Another error."]
        detail = get_validation_error_detail(
            DjangoValidationError(error),
        )
        self.assertEqual(
            detail,
            {
                "non_field_errors": [
                    "This is an error.",
                    "Another error."
                ]
            }
        )

    def test_django_dict_error(self):
        error = {
            "first_name": "This is required.",
            "last_name": [
                "This is too long.",
                "This is not correct."
            ]
        }
        detail = get_validation_error_detail(
            DjangoValidationError(error),
        )
        self.assertEqual(
            detail,
            {
                "first_name": ["This is required."],
                "last_name": [
                    "This is too long.",
                    "This is not correct."
                ]
            }
        )

    def test_django_non_field_errors(self):
        error = {
            DJANGO_NON_FIELD_ERRORS_KEY: "This is required.",
        }
        detail = get_validation_error_detail(
            DjangoValidationError(error),
        )
        self.assertEqual(
            detail,
            {"non_field_errors": ["This is required."]}
        )

    def test_drf_single_error(self):
        error = "This is an error."
        detail = get_validation_error_detail(
            DjangoValidationError(error)
        )
        self.assertEqual(
            detail,
            {
                "non_field_errors": [
                    "This is an error."
                ]
            }
        )

    def test_drf_list_error(self):
        error = ["This is an error.", "Another error."]
        detail = get_validation_error_detail(
            serializers.ValidationError(error),
        )
        self.assertEqual(
            detail,
            {
                "non_field_errors": [
                    "This is an error.",
                    "Another error."
                ]
            }
        )

    def test_drf_dict_error(self):
        error = {
            "first_name": "This is required.",
            "last_name": [
                "This is too long.",
                "This is not correct."
            ]
        }
        detail = get_validation_error_detail(
            serializers.ValidationError(error),
        )
        self.assertEqual(
            detail,
            {
                "first_name": ["This is required."],
                "last_name": [
                    "This is too long.",
                    "This is not correct."
                ]
            }
        )

    def test_drf_non_field_errors(self):
        error = {
            api_settings.NON_FIELD_ERRORS_KEY: "This is required.",
        }
        detail = get_validation_error_detail(
            serializers.ValidationError(error),
        )
        self.assertEqual(
            detail,
            {"non_field_errors": ["This is required."]}
        )

    def test_all_non_field_errors(self):
        error = {
            DJANGO_NON_FIELD_ERRORS_KEY: "This is required.",
            api_settings.NON_FIELD_ERRORS_KEY: "This is a problem.",
        }
        detail = get_validation_error_detail(
            serializers.ValidationError(error),
        )
        self.assertEqual(
            detail,
            {"non_field_errors": ["This is a problem.", "This is required."]}
        )


class CustomModelSerializerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class MyModel(models.Model):
            name = models.CharField(max_length=255)
            last_name = models.CharField(max_length=255)

            def clean(self):
                super().clean()
                raise DjangoValidationError({
                    "name": "There's a problem here."
                })

            def save(self, *args, **kwargs):
                self.full_clean()
                super().save(*args, **kwargs)

        cls.model_class = MyModel

        class MySerializer(CustomModelSerializer):
            first_name = serializers.CharField()

            model_field_name_mapping = dict(
                name="first_name",
            )

            class Meta:
                model = MyModel
                fields = ('first_name', 'last_name',)

        cls.serializer_class = MySerializer

    def test_validation_error(self):
        """Remap field validation errors that happen on serializer validation"""

        serializer = self.serializer_class(data={
            "last_name": "Smith",
        })
        with self.assertRaises(serializers.ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            ctx.exception.detail,
            {"first_name": ["This field is required."]}
        )

    def test_validated_data(self):
        """Remap field data on serializer validation"""

        serializer = self.serializer_class(data={
            "first_name": "John",
            "last_name": "Smith",
        })
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            serializer.validated_data,
            {
                "name": "John",
                "last_name": "Smith",
            }
        )

    def test_creation_error(self):
        """Remap field validation errors that happen on model creation"""

        serializer = self.serializer_class(data={
            "first_name": "John",
            "last_name": "Smith",
        })
        serializer.is_valid(raise_exception=True)
        with self.assertRaises(DjangoValidationError) as ctx:
            serializer.save()
        self.assertEqual(
            str(ctx.exception.error_dict),
            str({"first_name": [DjangoValidationError(["There's a problem here."])]})
        )

    def test_update_error(self):
        """Remap field validation errors that happen on model update"""

        obj = self.model_class()
        serializer = self.serializer_class(data={
            "first_name": "John",
            "last_name": "Smith",
        }, instance=obj)
        serializer.is_valid(raise_exception=True)
        with self.assertRaises(DjangoValidationError) as ctx:
            serializer.save()
        self.assertEqual(
            str(ctx.exception.error_dict),
            str({"first_name": [DjangoValidationError(["There's a problem here."])]})
        )


class CustomSerializerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class MySerializer(CustomSerializer):
            first_name = serializers.CharField()

            field_name_mapping = dict(
                first_name="name",
            )

        cls.serializer_class = MySerializer

    def test_validation_error(self):
        """Remap field validation errors that happen on serializer validation"""

        serializer = self.serializer_class(data={
            "last_name": "Smith",
        })
        with self.assertRaises(serializers.ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(
            ctx.exception.detail,
            {"first_name": ["This field is required."]}
        )

    def test_validated_data(self):
        """Remap field data on serializer validation"""

        serializer = self.serializer_class(data={
            "first_name": "John",
        })
        serializer.is_valid(raise_exception=True)
        self.assertEqual(
            serializer.validated_data,
            {"name": "John"}
        )


class CustomExceptionHandlerTest(TestCase):

    def test_exception_error(self):
        error = "This is an error."
        response = custom_exception_handler(
            exc=Exception(error), context={},
        )
        self.assertEqual(response, None)

    def test_django_validation_error(self):
        error = "This is an error."
        response = custom_exception_handler(
            exc=DjangoValidationError(error), context={},
        )
        self.assertEqual(
            response.data,
            {"non_field_errors": ["This is an error."]}
        )

    def test_drf_validation_error(self):
        error = "This is an error."
        response = custom_exception_handler(
            exc=serializers.ValidationError(error), context={},
        )
        self.assertEqual(
            response.data,
            {"non_field_errors": ["This is an error."]}
        )
