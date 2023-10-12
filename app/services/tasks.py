import time
from services import models as services_models
from celery import shared_task
from services import utils as services_utils
from settings.settings import WIQ_API_URL, WIQ_API_KEY, GLOBALSMM_API_URL, GLOBALSMM_API_KEY


SERVICE_CLIENTS = {
    # Подання відповідності сервісу до клієнта
    'WiQ': services_utils.WiQApiClient(WIQ_API_URL, WIQ_API_KEY),
    'GlobalSmm': services_utils.GlobalApiClient(GLOBALSMM_API_URL, GLOBALSMM_API_KEY)
}


@shared_task
def handlering_order(order_id):
    # Збір даних про замовлення.
    order = services_models.Order.objects.get(id=order_id)

    client = order.client
    self_to_service = order.service_type.get_self_to_service_display()
    service_id = order.service_type.service_id
    quantity = order.count
    link = order.url
    price = order.price

    # Відправка замовлення.
    execution_client = SERVICE_CLIENTS.get(self_to_service)
    order_from_client = execution_client.create_order(service_id, quantity, link)

    # Запис результату.
    try:
        order_success = order_from_client.get('success')
    except AttributeError:
        return f'Ошибка!!! Заказ номер №{order.id}'

    order_id = order_from_client.get('order')
    if order_success:
        order.order_id = order_id
        order.status = 'processing'
        order.save()
    else:
        status = order_from_client.get('error')
        if status != 'balance_error':
            client.balance += price
            client.save()
        order.status = status
        order.save()

    return f'Обработан заказ номер №{order.id}'


@shared_task
def rehadlering_invalid_orders():
    invalid_orders = services_models.Order.objects.filter(status='balance_error')
    quantity_of_invalid_order = len(invalid_orders)

    if quantity_of_invalid_order:
        for order in invalid_orders:
            handlering_order.delay(order.id)
            time.sleep(2)
        return f'На повторную обработку отправлено {quantity_of_invalid_order} заказ(a-ов).'
    return 'Инвалидных заказов не обнаружено.'


@shared_task
def checking_completed_orders():
    processing_orders = services_models.Order.objects.filter(status='processing')

    if processing_orders:
        for order in processing_orders:
            self_to_service = order.service_type.get_self_to_service_display()
            execution_client = SERVICE_CLIENTS.get(self_to_service)
            order_id = order.order_id

            order_data = execution_client.get_status(order_id)
            order.status = order_data.get('status')
            order.save()

            time.sleep(2)

        return f'Выполнена проверка {len(processing_orders)} заказa(ов).'
    return 'Заказов в обработке не обнаружено.'
