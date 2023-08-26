# from django.contrib import admin
from django.urls import path
from comments import views as comment_views


"""
Посилання програми.
"""
urlpatterns = [
    path('', view=comment_views.CommentsView.as_view(), name='comments'),
    path('create', view=comment_views.CreateCommentView.as_view(), name='create_comment'),
]
