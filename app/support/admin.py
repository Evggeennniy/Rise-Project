from django.contrib import admin
from support import models as support_models


@admin.register(support_models.SupportMail)
class SupportAdmin(admin.ModelAdmin):
    """
    Работа с базой данных підтримки.
    """

    # Поля виведення загального списку.
    list_display = (
        'client',
        'thema',
        'question',
        'answer',
        'notes',
        'data'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'client',
        'client_id',
        'client_username',
        'thema',
        'notes'
    )

    # Поля лише для читання.
    readonly_fields = (
        
    )
