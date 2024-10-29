from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend as DjangoModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


UserModel = get_user_model()


class ModelBackend(DjangoModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate users based on email and password. Only users with
        is_active=True are allowed. Only email addresses with is_verified=True
        is allowed.
        """
        if username is None:
            username = kwargs.get(UserModel.EMAIL_FIELD)
        try:
            validate_email(username)
        except ValidationError:
            return
        else:
            filter_params = {UserModel.EMAIL_FIELD: username}

        try:
            user = UserModel._default_manager.get(**filter_params)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
