# from django.shortcuts import render
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from comments import models as comments_models
from comments import forms as comments_form
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from app_utils import mixins


class CommentsView(mixins.CacheQuerysetMixin, generic.ListView):
    """
    Перегляд для сторінки коментарів.
    """
    cached_queryset_key = 'comments_queryset'
    cache_time = 60 * 5
    queryset = comments_models.Comment.objects.select_related('client').filter(is_active=True)
    ordering = 'id'
    template_name = 'comments.html'


class CreateCommentView(LoginRequiredMixin, generic.CreateView):
    """
    Вигляд для створення коментаря.
    """
    queryset = comments_models.Comment.objects
    form_class = comments_form.CommentForm
    template_name = 'create_comment.html'
    success_url = reverse_lazy('comments')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client_id'] = self.request.user.id
        return kwargs
