# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from support import forms as support_forms
from support import models as support_models
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator


class SupportMailView(LoginRequiredMixin, generic.ListView):
    queryset = support_models.SupportMail.objects
    template_name = 'supportmail.html'

    def get_queryset(self):
        queryset = self.queryset.filter(
            client_id=self.request.user.id,
        )

        return queryset


class CreateSupportMailView(LoginRequiredMixin, generic.CreateView):
    queryset = support_models.SupportMail.objects
    form_class = support_forms.SupportMailForm
    success_url = reverse_lazy('support_mails')

    template_name = "createsupportmail.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client_id'] = self.request.user.id

        return kwargs
