from django.contrib import admin
from comments import models as comments_models


@admin.register(comments_models.Comment)
class CommentsAdmin(admin.ModelAdmin):
    """
    Робота з базою даних відгуків.
    """

    # Поля виведення загального списку.
    list_display = (
        'client',
        'rating',
        'comment',
        'data',
        'is_active'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'client',
        'client_username',
        'client_id',
        'comment',
        'rating',
    )

    # Поля лише для читання.
    readonly_fields = (
        
    )