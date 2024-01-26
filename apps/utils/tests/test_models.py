from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import connection, IntegrityError
from django.db.models.base import ModelBase
from django.utils import timezone

from apps.utils.models import (
    JSONObjectField,
    JSONObjectFormField,
    JSONArrayField,
    JSONArrayFormField,
    CreatedModifiedModel,
)


class ModelMixinTestCase(TestCase):
    # Source: https://stackoverflow.com/a/45239964/3769045
    mixins = ()

    @classmethod
    def setUpClass(cls):
        # # Create a dummy model which extends the mixin
        cls.Model = ModelBase(
            "__TestModel__" + cls.mixins[0].__name__,
            cls.mixins,
            {"__module__": cls.mixins[0].__module__},
        )
        # Create the schema for our test model
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls.Model)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Delete the schema for the test model
        with connection.schema_editor() as schema_editor:
            connection.disable_constraint_checking()
            schema_editor.delete_model(cls.Model)


class CreatedModifiedModelTest(ModelMixinTestCase):
    mixins = (CreatedModifiedModel,)

    def test_create(self):
        obj = self.Model()
        # Create
        obj.save()
        self.assertIsNotNone(obj.created_at)
        self.assertEqual(obj.created_at, obj.modified_at)

    def test_create_null_created_at(self):
        obj = self.Model(created_at=None)
        # Create
        with self.assertRaises(IntegrityError):
            obj.save()

    def test_create_null_modified_at(self):
        obj = self.Model(modified_at=None)
        # Create
        obj.save()
        self.assertIsNotNone(obj.modified_at)
        self.assertEqual(obj.created_at, obj.modified_at)

    def test_create_custom_created_at(self):
        custom_ts = timezone.now()
        obj = self.Model(created_at=custom_ts)
        # Create
        obj.save()
        self.assertIsNotNone(obj.created_at)
        self.assertEqual(obj.created_at, custom_ts)
        self.assertEqual(obj.created_at, obj.modified_at)

    def test_create_custom_modified_at(self):
        custom_ts = timezone.now()
        obj = self.Model(modified_at=custom_ts)
        # Create
        obj.save()
        self.assertIsNotNone(obj.modified_at)
        self.assertNotEqual(obj.modified_at, custom_ts)
        self.assertEqual(obj.created_at, obj.modified_at)

    def test_update(self):
        obj = self.Model()
        # Create
        obj.save()
        # Update
        obj.save()
        self.assertIsNotNone(obj.modified_at)
        self.assertTrue(obj.modified_at > obj.created_at)

    def test_bulk_create(self):
        bulk_list = [self.Model()] * 2
        self.Model.objects.bulk_create(bulk_list)
        obj = self.Model.objects.first()
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.modified_at)
        self.assertTrue(obj.created_at <= obj.modified_at)


class JSONObjectFieldTest(TestCase):

    def test_deny_empty_value(self):
        empty_values = [""]
        field = JSONObjectField(blank=False)
        for empty_value in empty_values:
            with self.assertRaisesMessage(
                ValidationError, "This field cannot be blank."
            ):
                field.clean(empty_value, None)

    def test_allow_empty_invalid_value(self):
        empty_values = [""]
        field = JSONObjectField(blank=True)
        for empty_value in empty_values:
            with self.assertRaisesMessage(
                ValidationError, "Value must be a valid JSON object."
            ):
                field.clean(empty_value, None)

    def test_deny_null_value(self):
        field = JSONObjectField(blank=True, null=False)
        with self.assertRaisesMessage(ValidationError, "This field cannot be null."):
            field.clean(None, None)

    def test_allow_null_value(self):
        field = JSONObjectField(blank=True, null=True)
        value = field.clean(None, None)
        self.assertEqual(value, None)

    def test_valid_value(self):
        field = JSONObjectField(null=True)
        input_values = [{}, {"a": 1, "b": 2.5}]
        for input_value in input_values:
            with self.subTest(input_value=input_value):
                value = field.clean(input_value, None)
                self.assertEqual(field.clean(value, None), value)

    def test_invalid_value(self):
        field = JSONObjectField()
        input_values = [
            (),
            "()",
            [],
            "[]",
            ["a", "b", 3],
            '["a", "b", 3]',
            "{1}",
            "Hello, World!",
            1,
            2.5,
        ]
        for input_value in input_values:
            with self.assertRaises(ValidationError) as ctx:
                field.clean(input_value, None)
            self.assertEqual(
                ctx.exception.messages, ["Value must be a valid JSON object."]
            )

    def test_formfield(self):
        model_field = JSONObjectField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, JSONObjectFormField)

    def test_deny_empty_deny_null_formfield(self):
        model_field = JSONObjectField(blank=False, null=False)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_allow_empty_deny_null_formfield(self):
        model_field = JSONObjectField(blank=True, null=False)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_deny_empty_allow_null_formfield(self):
        model_field = JSONObjectField(blank=False, null=True)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_allow_empty_allow_null_formfield(self):
        model_field = JSONObjectField(blank=True, null=True)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, False)


class JSONObjectFormFieldTest(TestCase):

    def test_deny_empty_value(self):
        empty_values = [None, "", "null"]
        field = JSONObjectFormField(required=True)
        for empty_value in empty_values:
            with self.assertRaisesMessage(ValidationError, "This field is required."):
                field.clean(empty_value)

    def test_allow_empty_value(self):
        empty_values = [None, "", "null"]
        field = JSONObjectFormField(required=False)
        for empty_value in empty_values:
            with self.subTest(empty_value=empty_value):
                value = field.clean(empty_value)
                self.assertEqual(value, None)

    def test_valid_value(self):
        field = JSONObjectFormField()
        input_values = [{}, "{}", {"a": 1, "b": 2.5}, '{"a": 1, "b": 2.5}']
        for input_value in input_values:
            with self.subTest(input_value=input_value):
                value = field.clean(input_value)
                self.assertEqual(field.clean(value), value)

    def test_invalid_value(self):
        field = JSONObjectFormField()
        input_values = [
            (),
            "()",
            [],
            "[]",
            ["a", "b", 3],
            '["a", "b", 3]',
            "{1}",
            "Hello, World!",
            1,
            2.5,
        ]
        for input_value in input_values:
            with self.assertRaises(ValidationError) as ctx:
                field.clean(input_value)
            self.assertEqual(
                ctx.exception.messages,
                [f"'{input_value}' value must be a valid JSON object."],
            )


class JSONArrayFieldTest(TestCase):

    def test_deny_empty_value(self):
        empty_values = [""]
        field = JSONArrayField(blank=False)
        for empty_value in empty_values:
            with self.assertRaisesMessage(
                ValidationError, "This field cannot be blank."
            ):
                field.clean(empty_value, None)

    def test_allow_empty_invalid_value(self):
        empty_values = [""]
        field = JSONArrayField(blank=True)
        for empty_value in empty_values:
            with self.assertRaisesMessage(
                ValidationError, "Value must be a valid JSON array."
            ):
                field.clean(empty_value, None)

    def test_deny_null_value(self):
        field = JSONArrayField(blank=True, null=False)
        with self.assertRaisesMessage(ValidationError, "This field cannot be null."):
            field.clean(None, None)

    def test_allow_null_value(self):
        field = JSONArrayField(blank=True, null=True)
        value = field.clean(None, None)
        self.assertEqual(value, None)

    def test_valid_value(self):
        field = JSONArrayField(null=True)
        input_values = [[], ["a", 1, "b", 2.5]]
        for input_value in input_values:
            with self.subTest(input_value=input_value):
                value = field.clean(input_value, None)
                self.assertEqual(field.clean(value, None), value)

    def test_invalid_value(self):
        field = JSONArrayField()
        input_values = [
            (),
            "()",
            {},
            "{}",
            {"a": 1, "b": 2.5},
            '{"a": 1, "b": 2.5}',
            "{1}",
            "Hello, World!",
            1,
            2.5,
        ]
        for input_value in input_values:
            with self.assertRaises(ValidationError) as ctx:
                field.clean(input_value, None)
            self.assertEqual(
                ctx.exception.messages, ["Value must be a valid JSON array."]
            )

    def test_formfield(self):
        model_field = JSONArrayField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, JSONArrayFormField)

    def test_deny_empty_deny_null_formfield(self):
        model_field = JSONArrayField(blank=False, null=False)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_allow_empty_deny_null_formfield(self):
        model_field = JSONArrayField(blank=True, null=False)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_deny_empty_allow_null_formfield(self):
        model_field = JSONArrayField(blank=False, null=True)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, True)

    def test_allow_empty_allow_null_formfield(self):
        model_field = JSONArrayField(blank=True, null=True)
        form_field = model_field.formfield()
        self.assertEqual(form_field.required, False)


class JSONArrayFormFieldTest(TestCase):

    def test_deny_empty_value(self):
        empty_values = [None, "", "null"]
        field = JSONArrayFormField(required=True)
        for empty_value in empty_values:
            with self.assertRaisesMessage(ValidationError, "This field is required."):
                field.clean(empty_value)

    def test_allow_empty_value(self):
        empty_values = [None, "", "null"]
        field = JSONArrayFormField(required=False)
        for empty_value in empty_values:
            with self.subTest(empty_value=empty_value):
                value = field.clean(empty_value)
                self.assertEqual(value, None)

    def test_valid_value(self):
        field = JSONArrayFormField()
        input_values = [[], "[]", ["a", 1, "b", 2.5], '["a", 1, "b", 2.5]']
        for input_value in input_values:
            with self.subTest(input_value=input_value):
                value = field.clean(input_value)
                self.assertEqual(field.clean(value), value)

    def test_invalid_value(self):
        field = JSONArrayFormField()
        input_values = [
            (),
            "()",
            {},
            "{}",
            {"a": 1, "b": 2.5},
            '{"a": 1, "b": 2.5}',
            "{1}",
            "Hello, World!",
            1,
            2.5,
        ]
        for input_value in input_values:
            with self.assertRaises(ValidationError) as ctx:
                field.clean(input_value)
            self.assertEqual(
                ctx.exception.messages,
                [f"'{input_value}' value must be a valid JSON array."],
            )
