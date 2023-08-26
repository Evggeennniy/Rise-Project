# from django.contrib import admin
from django.urls import path
from services import views as services_views


"""
Посилання програми.
"""
urlpatterns = [
    path('services_categories', services_views.ServiceCategoryView.as_view(), name='services_category'),
    path('create_order/<int:pk>', services_views.ServiceOrderCreate.as_view(), name='create_service_order'),
]
