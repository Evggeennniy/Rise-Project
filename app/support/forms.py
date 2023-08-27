from django import forms
from support import models as support_models


class SupportMailForm(forms.ModelForm):
    """
    Форма для надсилання листів підтримки.
    """

    thema = forms.CharField(
        label='Тема',
        min_length=6,
        max_length=64,
        help_text='Коротко вкажіть із чим пов\'язана ваша проблема.',
        required=True
    )
    question = forms.CharField(
        label='Описание',
        min_length=30,
        max_length=256,
        help_text='Опишіть, що вас цікавить.',
        widget=forms.Textarea(),
        required=True
    )
    notes = forms.CharField(
        label='Примітки',
        min_length=0,
        max_length=64,
        help_text='Номер замовлення тощо.',
        required=False
    )
    report = forms.ImageField(
        label='Репорт',
        help_text='Ви можете прикріпити скріншот.',
        required=False
    )

    # Модель роботи і поля для отримання.
    class Meta:
        model = support_models.SupportMail
        fields = (
            'thema',
            'question',
            'notes',
            'report'
        )

    # Ініціалізація.
    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client_id')
        super().__init__(*args, **kwargs)

    # Сохранение в базу.
    def save(self, commit=True):
        commit_data = super().save(commit=False)
        commit_data.__dict__['client_id'] = self.client
        commit_data = super().save(commit=True)

        return commit_data