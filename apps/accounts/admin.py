from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models, forms
from .forms import AuthenticationForm


admin.site.login_form = AuthenticationForm


# Register your models here.
@admin.register(models.User)
class UserAdmin(UserAdmin):
    add_form = forms.CreateUserForm
    add_form_template = "admin/accounts/user/add_form.html"
    list_display = (
        "uuid",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )
    search_fields = (
        "uuid",
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("-date_joined",)
    readonly_fields = (
        "uuid",
        "last_login",
        "date_joined",
    )

    fieldsets = (
        (None, {"fields": ("uuid", "email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name"),
            },
        ),
    )
