from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts import choices as account_choises


class User(AbstractUser):
    """
    База даних для користувачів
    """
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ('email',)

    username = models.CharField(verbose_name='Нікнейм', max_length=35, unique=True, null=False)
    email = models.CharField(verbose_name='Пошта', max_length=128, unique=False, null=False, blank=True)

    profile_status = models.CharField(verbose_name='Cтатус профiля',
                                      choices=account_choises.CLIENT, max_length=15, default='regular')

    balance = models.DecimalField(verbose_name='Баланс', max_digits=10, decimal_places=2, default=0.0)

    def enough_balance(self, order_price):
        if order_price > self.balance:
            return False
        return True


class Payment(models.Model):
    """
    Модель бази даних платежiв.
    """
    client = models.ForeignKey(verbose_name='Клiент', to='accounts.User', on_delete=models.CASCADE, null=True)
    value = models.DecimalField(verbose_name='Cума', max_digits=10, decimal_places=2)
    screenshot = models.ImageField(verbose_name='Cкриншот', upload_to='screenshots', default=None)
    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return f'Платiж {self.id}, сума {self.value}, дата {self.data}'

    class Meta:
        verbose_name = 'Платiж'
        verbose_name_plural = 'Платежi'
