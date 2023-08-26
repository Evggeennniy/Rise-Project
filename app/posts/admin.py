from django.contrib import admin
from posts import models as posts_models


@admin.register(posts_models.Post)
class PostsAdmin(admin.ModelAdmin):
    """
    Робота з базою даних постів.
    """

    # Поля виведення загального списку.
    list_display = (
        'header',
        'short_description',
        'data'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'header',
    )

    # Поля лише для читання.
    readonly_fields = (
        
    )

