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
    email = models.CharField(verbose_name='Пошта', max_length=128, unique=False, null=False)

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
    fonds = models.CharField(verbose_name='Валюта', choices=account_choises.FONDS, default='USD', max_length=5)
    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True)

    status = models.CharField(verbose_name='Статус', choices=account_choises.PAYMENT_STATUS, default='created', max_length=15)
    
    def __str__(self) -> str:
        return f'Платiж {self.id}, сума {self.value} {self.fonds}, дата {self.data}'

    class Meta:
        verbose_name = 'Платiж'
        verbose_name_plural = 'Платежi'
