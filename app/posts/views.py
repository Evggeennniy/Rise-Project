# from django.shortcuts import render
from django.views import generic
from posts import models as posts_models
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from app_utils import mixins


class PostsView(mixins.CacheQuerysetMixin, generic.ListView):
    """
    Перегляд для головної сторінки.
    """
    cached_queryset_key = 'posts_queryset'
    cache_time = 60 * 5
    queryset = posts_models.Post.objects
    ordering = 'id'
    template_name = 'posts.html'


class PostDetailView(mixins.CacheQuerysetMixin, generic.DetailView):
    """
    Перегляд для постов.
    """
    cached_queryset_key = 'posts_detail_queryset'
    cache_time = 60 * 5
    queryset = posts_models.Post.objects
    template_name = 'post_detail.html'