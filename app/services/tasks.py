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
    self_to = order.service_type.get_self_to_service_display()
    service_id = order.service_type.service_id
    quantity = order.count
    link = order.url

    # Відправка замовлення.
    execution_client = SERVICE_CLIENTS.get(self_to)
    order_from_client = execution_client.create_order(service_id, quantity, link)

    # Запис результату.
    order_info = order_from_client.get('order')
    order_success = order_from_client.get('success')
    if order_success is True:
        order.order_id = order_info
        order.status = 1
        order.save()
        return f'Отправлен заказ номер №{order.id}'
    elif order_info == 'balance_error':
        order.status = 3
        order.save()
    elif order_info == 'id_error':
        order.status = 4
        order.save()
        return f'В заказе отказано №{order.id}'
    elif order_info == 'unknown_error':
        order.status = 5
        order.save()
        return f'Неизвестная ошибка №{order.id}'
    

@shared_task
def rehadlering_invalid_orders():
    invalid_orders = services_models.Order.objects.filter(status=3)
    quantity_of_invalid_order = len(invalid_orders)

    if quantity_of_invalid_order:
        for order in invalid_orders:
            order.status = 1
            order.save()
            handlering_order.delay(order.id)
            time.sleep(2)
        return f'На повторную обработку отправлено {quantity_of_invalid_order} заказ(a-ов).'
    return 'Инвалидных заказов не обнаружено.'


@shared_task
def checking_completed_orders():
    processing_orders = services_models.Order.objects.filter(status=1)

    if processing_orders:
        for order in processing_orders:
            self_to = order.service_type.get_self_to_service_display()
            execution_client = SERVICE_CLIENTS.get(self_to)
            order_id = order.order_id

            order_data = execution_client.get_status(order_id)
            status = order_data.get('status')

            if status == 'completed':
                order.status = 2
                order.save()
            elif status == 'canceled':
                order.status = 6
                order.save()
            time.sleep(2)

        return f'Выполнена проверка {len(processing_orders)} заказa(ов).'
    return 'Заказов в обработке не обнаружено.'
