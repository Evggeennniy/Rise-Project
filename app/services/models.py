from django.db import models
from services import choices as services_choices
from accounts import choices as accounts_choices


class SocialNetwork(models.Model):
    """
    База даних для збереження соціальних мереж.
    """
    logo = models.ImageField(verbose_name='Лого', upload_to='logos', default=None)
    name = models.CharField(verbose_name='Назва', max_length=16)
    description = models.CharField(verbose_name='Опис', max_length=80, default='')
    is_active = models.BooleanField(verbose_name='Активна категорія', default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Соціальна мережа'
        verbose_name_plural = 'Соціальні мережі'


class Service(models.Model):
    """
    База даних для збереження послуг.
    """
    social_network = models.ForeignKey(verbose_name='Соціальна мережа',
                                    to='services.SocialNetwork', on_delete=models.CASCADE)
    service_logo = models.ImageField(verbose_name='Лого', upload_to='service_logos', default=None)
    service_name = models.CharField(verbose_name='Послуга', max_length=32)
    min_count = models.PositiveIntegerField(verbose_name='Мінімальна кількість')

    def __str__(self) -> str:
        return f'{self.social_network.name} - {self.service_name}'

    class Meta:
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'


class ServiceType(models.Model):
    """
    База даних для збереження типв послуг.
    """
    service_type = models.ForeignKey(verbose_name='Тип послуги', to='services.Service', on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Вид', max_length=32)
    self_to_client = models.CharField(verbose_name='Вiдношення до типу клiентiв',
                                      choices=accounts_choices.CLIENT, max_length=15, default='regular')
    price_per_1000 = models.DecimalField(verbose_name='Ціна за тисячу ($)', default=0.0, max_digits=8, decimal_places=2)

    self_to_service = models.CharField(verbose_name='Вiдношення до сервiсу',
                                       choices=services_choices.SERVICE, max_length=15, default='wiq')
    service_id = models.IntegerField(verbose_name='Код послуги (id)', default=0)

    def __str__(self) -> str:
        return f'{self.type} ціна за тисячу {self.price_per_1000} USD'

    class Meta:
        verbose_name = 'Тип послуги'
        verbose_name_plural = 'Типи послуги'


class Order(models.Model):
    """
    База даних для збереження замовлень.
    """
    client = models.ForeignKey(verbose_name='Клієнт', to='accounts.User', on_delete=models.CASCADE)
    service = models.ForeignKey(verbose_name='Послуга', to='services.Service', on_delete=models.DO_NOTHING)
    service_type = models.ForeignKey(verbose_name='Тип послуги', to='services.ServiceType', on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField(verbose_name='Кількість')
    url = models.URLField(verbose_name='Посилання', default='', blank=True)
    price = models.DecimalField(verbose_name='Ціна', max_digits=10, decimal_places=2, default=0.0, blank=True)

    order_id = models.CharField(verbose_name='Номер заказу', max_length=32, blank=True)
    status = models.CharField(verbose_name='Статус', choices=services_choices.ORDER_STATUS,
                              default='created', max_length=16)

    data = models.DateTimeField(verbose_name='Дата', auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return f'Послуга {self.service.service_name}, Кількість {self.count}, Ціна {self.price} '

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'


class Footer(models.Model):
    """
    База даних для футера.
    """
    header = models.CharField(verbose_name='Заголовок', max_length=32)
    url = models.CharField(verbose_name='Посилання', max_length=128, default='#')

    def __str__(self) -> str:
        return self.header

    class Meta:
        verbose_name = 'Информація'
        verbose_name_plural = 'Информація'
