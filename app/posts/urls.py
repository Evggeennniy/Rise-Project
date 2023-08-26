# from django.contrib import admin
from django.urls import path
from posts import views as posts_views


"""
Посилання програми.
"""
urlpatterns = [
    path('', view=posts_views.PostsView.as_view(), name='posts'),
    path('detail/<int:pk>', view=posts_views.PostDetailView.as_view(), name='post_detail'),
]
