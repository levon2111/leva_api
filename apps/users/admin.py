from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'phone',
        'zip_code',
        'email',
        'email_confirmation_token',
        'reset_key',
    ]

    search_fields = [
        'username',
        'first_name',
        'last_name',
        'phone',
        'email',
    ]

    list_filter = [
        'created_at'
    ]

    class Meta:
        model = User
