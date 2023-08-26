# from django.contrib import admin
from django.urls import path
from support import views as support_views


"""
Посилання програми.
"""
urlpatterns = [
    path('mails', support_views.SupportMailView.as_view(), name='support_mails'),
    path('create_support_mail', support_views.CreateSupportMailView.as_view(), name='create_support_mail')
]
