# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from services import models as services_models
from services import forms as services_forms
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from app_utils import mixins


class IndexView(mixins.CacheQuerysetMixin, generic.ListView):
    """
    Перегляд для головної сторінки.
    """
    cached_queryset_key = 'services_queryset'
    cache_time = 30 * 5
    queryset = services_models.SocialNetwork.objects
    ordering = 'id'
    template_name = 'index.html'


class ServiceCategoryView(mixins.CacheQuerysetMixin, generic.ListView):
    """
    Вид для категорії сервісу.
    """
    cached_queryset_key = 'service_categories_queryset'
    cache_time = 30 * 5
    queryset = services_models.Service.objects.select_related('social_network')
    ordering = 'social_network'
    template_name = 'services_category.html'


class ServiceOrderCreate(LoginRequiredMixin, mixins.CacheQuerysetMixin, generic.CreateView):
    """
    Вид для створення замовлення.
    """
    cached_queryset_key = 'services_create_order_queryset'
    cache_time = 30 * 5
    queryset = services_models.Service.objects
    form_class = services_forms.OrderForm
    success_url = reverse_lazy('index')
    template_name = "createserviceorder.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        service_id = self.kwargs['pk']

        kwargs['client_id'] = self.request.user.id
        kwargs['service_id'] = service_id
        kwargs['min_count'] = services_models.Service.objects.get(id=service_id).min_count
        
        kwargs['client_type'] = self.request.user.profile_status

        return kwargs
