from django import forms
from comments import models as comments_models
from comments import choises


class CommentForm(forms.ModelForm):
    """
    Форма для надсилання коментов.
    """

    rating = forms.ChoiceField(
        label='Рейтинг',
        choices=choises.RATING_CHOISES,
        help_text='Вкажіть оцінку сервісу.',
    )
    comment = forms.CharField(
        label='Відгук',
        min_length=10,
        max_length=256,
        help_text='Опишіть свій відгук.',
        widget=forms.Textarea(),
        required=True
    )

    # Модель роботи і поля для отримання.
    class Meta:
        model = comments_models.Comment
        fields = (
            'rating',
            'comment'
        )

    # Ініціалізація.
    def __init__(self, *args, **kwargs):
        self.client_id = kwargs.pop('client_id')
        super().__init__(*args, **kwargs)

    # Сохранение в базу.
    def save(self, commit=True):
        commit_data = super().save(commit=False)
        commit_data.__dict__['client_id'] = self.client_id
        commit_data = super().save(commit=True)

        return commit_data