from django.db import models


class Post(models.Model):
    """
    Модель бази даних постів.
    """
    header = models.CharField(verbose_name='Заголовок', max_length=32)
    short_description = models.CharField(verbose_name='Короткий опис', max_length=32)
    description = models.CharField(verbose_name='Опис', max_length=512)
    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True)
    
    def __str__(self) -> str:
        return f'Заголовок {self.header}, Опис {self.description}, Дата {self.data}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
