from typing import Any, Dict
from django import forms
# from liqpay3.liqpay import LiqPay
from services import models as service_models
from services import tasks as service_tasks
from accounts import models as account_models


class OrderForm(forms.ModelForm):
    """
    Форма для замовлень.
    """
    # Модель роботи і поля для отримання.
    class Meta:
        model = service_models.Order
        fields = (
            'count',
            'url',
            'service_type',
            'price'
        )

    # Ініціалізація.
    def __init__(self, *args, **kwargs):
        self.client_id = kwargs.pop('client_id')
        self.service_id = kwargs.pop('service_id')
        self.min_count = kwargs.pop('min_count')
        self.client_type = kwargs.pop('client_type')
        super().__init__(*args, **kwargs)

        self.fields['service_type'] = forms.ModelChoiceField(
            queryset=service_models.ServiceType.objects.filter(
                service_type_id=self.service_id,
                self_to_client=self.client_type
            ),
            label='Оберіть вид послуги',
            help_text='Виберіть вид послуги.',
        )

        self.fields['url'] = forms.URLField(
            label='Посилання',
            help_text='Вкажіть посилання на профиль чи публикацию.',
        )

        self.fields['count'] = forms.IntegerField(
            label='Кількість',
            help_text='Вкажіть бажану кількість.',
        )

        self.fields['price'] = forms.DecimalField(
            label='Ціна',
            help_text='Загальна сума за замовлення',
            widget=forms.NumberInput(attrs={'readonly': 'readonly'})
        )

    # Валідація
    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['count'] < self.min_count:
                raise forms.ValidationError(f'Мінімальна кількість для цієї послуги {self.min_count}')

            user = account_models.User.objects.get(id=self.client_id)
            price_of_order = cleaned_data['price']

            if not user.enough_balance(price_of_order) :
                raise forms.ValidationError('Недостатній баланс!')
            
            user.balance -= price_of_order
            user.save()

        return cleaned_data

    # Збереження у основу.
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.__dict__['client_id'] = self.client_id
        instance.__dict__['service_id'] = self.service_id
        instance = super().save(commit)

        # Відправлення на обробку.
        service_tasks.handlering_order.delay(instance.id)
        
        return instance
