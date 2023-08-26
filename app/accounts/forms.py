from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from accounts import choices as account_choises
from accounts import models as account_models


class SignUpForm(forms.ModelForm):
    """
    Форма для реєстрації.
    """

    username = forms.CharField(
        label='Нікнейм',
        min_length=6,
        max_length=35
    )
    email = forms.CharField(
        label='Пошта',
        min_length=8,
        max_length=128
    )
    password = forms.CharField(
        label='Пароль',
        min_length=6,
        max_length=35,
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label='Повторно пароль',
        min_length=6,
        max_length=35,
        widget=forms.PasswordInput
    )

    # Модель для роботи та поля для отримання.
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',

            'password',
            'confirm_password',
        )

    # Валідація одержаних даних.
    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['confirm_password']:
                raise forms.ValidationError('Паролі не співпадають!')

        return cleaned_data

    # Збереження у основу.
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password'])

        if commit:
            instance.save()

        return instance


class ChoosePaymentForm(forms.ModelForm):
    """
    Форма для вибору варианту плати.
    """

    # Ініціалізація.
    def __init__(self, *args, **kwargs):
        self.client_id = kwargs.pop('client_id')
        return super().__init__(*args, **kwargs)

    # Модель для роботи та поля для отримання.
    class Meta:
        model = account_models.Payment
        fields = (
            'value',
            'fonds'
        )
        
        # Збереження у основу.
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.__dict__['client_id'] = self.client_id

        if commit:
            instance.save()

        return instance