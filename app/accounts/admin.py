from django.contrib import admin
from accounts import models as account_models


@admin.register(account_models.User)
class UsersAdmin(admin.ModelAdmin):
    """
    Робота з базою даних користувачів в адмін меню.
    """

    # Поля виведення загального списку.
    list_display = (
        'username',
        'profile_status',
        'balance',
        'id',
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'id',
        'email',
        'username',
        'profile_status'
    )

    # Поля лише для читання.
    readonly_fields = (
        
    )


@admin.register(account_models.Payment)
class PaymentsAdmin(admin.ModelAdmin):
    """
    Робота з базою даних користувачів в адмін меню.
    """

    # Поля виведення загального списку.
    list_display = (
        'client',
        'id',
        'value',
        'fonds',
        'data',
        'status'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'id',
        'client',
        'value',
        'fonds',
        'data',
        'status'
    )

    # Поля лише для читання.
    readonly_fields = (
        
    )
