from django.db import models
from comments import choises


class Comment(models.Model):
    """
    База даних для збереження коментарів.
    """
    client = models.ForeignKey(verbose_name='Клієнт', to='accounts.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(verbose_name='Рейтинг', choices=choises.RATING_CHOISES)
    comment = models.CharField(verbose_name='Відгук', max_length=256)
    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True)
    
    is_active = models.BooleanField(verbose_name='Активний', default=False)

    def get_rating(self):
        return range(1, self.rating+1)

    def __str__(self) -> str:
        return f'Рейтинг {self.rating}, Відгук {self.comment}, Дата {self.data}'

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'