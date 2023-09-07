from django.db import models


class SupportMail(models.Model):
    """
    Модель бази даних листів підтримки.
    """
    client = models.ForeignKey(verbose_name='Користувач', to='accounts.User', on_delete=models.CASCADE, )
    thema = models.CharField(verbose_name='Тема', max_length=32)
    question = models.TextField(verbose_name='Опис', max_length=512)
    notes = models.CharField(verbose_name='Примітки', max_length=64, blank=True)
    report = models.ImageField(verbose_name='Cкріншот', upload_to='reports', blank=True)
    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True,)

    answer = models.TextField(verbose_name='Відповідь', max_length=256, blank=True)

    def __str__(self) -> str:
        return f'Тема {self.thema}, Опис {self.question}, Дата {self.data}'

    class Meta:
        verbose_name = 'Лист підтримки'
        verbose_name_plural = 'Листи підтримки'
