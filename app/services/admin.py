from django.contrib import admin
from services import models as services_models


@admin.register(services_models.SocialNetwork)
class ServicesCategoryAdmin(admin.ModelAdmin):
    """
    Робота з базою даних категорiй.
    """

    # Поля виведення загального списку.
    list_display = (
        'name',
        'description',
        'is_active'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'name',
    )

    # Поля лише для читання.
    readonly_fields = (

    )


@admin.register(services_models.Service)
class ServicesAdmin(admin.ModelAdmin):
    """
    Робота з базою даних послуг в адмін меню.
    """

    # Поля виведення загального списку.
    list_display = (
        'social_network',
        'service_name',
        'min_count'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'social_network',
        'service_name'
    )

    # Поля лише для читання.
    readonly_fields = (

    )


@admin.register(services_models.ServiceType)
class ServiceTypesAdmin(admin.ModelAdmin):
    """
    Робота з базою даних  в адмін меню.
    """

    # Поля виведення загального списку.
    list_display = (
        'service_type',
        'type',
        'price_per_1000',
        'self_to_client',
        'self_to_service',
        'service_id'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'type',
        'self_to_client',
        'self_to_service',
        'service_id'
    )

    # Поля лише для читання.
    readonly_fields = (

    )


@admin.register(services_models.Order)
class OrdersAdmin(admin.ModelAdmin):
    """
    Робота з базою даних замовлень.
    """

    # Поля виведення загального списку.
    list_display = (
        'client',
        'service',
        'count',
        'price',
        'status',
        'order_id',
        'data'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'order_id',
        'price',
    )

    # Поля лише для читання.
    readonly_fields = (

    )


@admin.register(services_models.Footer)
class FootersAdmin(admin.ModelAdmin):
    """
    Робота з базою футеров.
    """

    # Поля виведення загального списку.
    list_display = (
        'header',
        'url'
    )

    # Поля за якими буде здійснюватися пошук.
    search_fields = (
        'header',
    )

    # Поля лише для читання.
    readonly_fields = (

    )
