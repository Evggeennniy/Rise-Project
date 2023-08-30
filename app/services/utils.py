import requests
from abc import ABC, abstractmethod


class ApiClient(ABC):
    """
    Класс для макета Api клиента.
    """

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def get_response(self, url, params) -> dict:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return f'Ошибка сервера. [{response.status_code}]'

    @abstractmethod
    def create_order(self) -> dict:
        pass

    @abstractmethod
    def get_status(self) -> dict:
        pass

    # @abstractmethod
    # def get_multiple_status(self) -> dict:
    #     pass


class WiQApiClient(ApiClient):
    """
    Класс для клиента Api к WiQ сервису.
    """

    def create_order(self, service_id, quantity, link) -> dict:
        params = {
            'key': self.api_key,
            'action': 'create',
            'service': service_id,
            'quantity': quantity,
            'link': link
        }
        response = self.get_response(self.url, params=params)
        order_id = response.get('order', False)
        error = response.get('Error', False)

        print(f'create order : {response} - WIQ')
        if order_id:
            response['success'] = True
            return response
        elif error == 'balance':
            response['success'] = False
            return dict(order='balance_error')
        elif error == 'Service does not exists.':
            response['success'] = False
            return dict(order='id_error')
        else:
            response['success'] = False
            return dict(order='unknown_error')

    def get_status(self, order_id) -> dict:
        params = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id,
        }
        response = self.get_response(self.url, params=params)
        status = response.get('status', False)

        print(f'create order : {response} - WIQ')
        if status == 'Processing' or status == 'In progress':
            return dict(status='processing')
        elif status == 'Completed':
            return dict(status='completed')


class GlobalApiClient(ApiClient):
    """
    Класс для клиента Api к GlobalSmm сервису.
    """

    def create_order(self, service_id, quantity, link) -> dict:
        params = {
            'key': self.api_key,
            'action': 'add',
            'service': service_id,
            'quantity': quantity,
            'link': link
        }
        response = self.get_response(self.url, params=params)
        order_id = response.get('order', False)
        error = response.get('error', False)

        print(f'create order : {response} - GLOBALSMM')
        if order_id:
            response['success'] = True
            return response
        elif error == 'neworder.error.not_enough_funds':
            response['success'] = False
            return dict(order='balance_error')
        elif error == 'error.incorrect_service_id':
            response['success'] = False
            return dict(order='id_error')
        else:
            response['success'] = False
            return dict(order='unknown_error')

    def get_status(self, order_id):
        params = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id,
        }
        response = self.get_response(self.url, params=params)
        status = response.get('status', False)

        print(f'status check : {response} - GLOBALSMM')
        if status == 'Partial' or status == 'In progress':
            return dict(status='processing')
        elif status == 'Completed':
            return dict(status='completed')

    # def get_multiple_status(self, *order_ids) -> dict:
    #     data_of_orders = dict()
    #     for order_id in order_ids:
    #         status = self.get_status(order_id)
    #         data_of_orders[order_id] = status
    #         time.sleep(3)

    #     return data_of_orders
