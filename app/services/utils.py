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

    errors = {
        'balance': 'balance_error',
        'Service does not exists.': 'id_error',
    }
    statuses = {
        'Processing': 'processing',
        'In progress': 'processing',
        'Pending': 'processing',
        'Completed': 'completed',
    }

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

        if order_id:
            response['success'] = True
        else:
            response['success'] = False
            error = response.get('Error')
            response['error'] = self.errors.get(error, 'not_known')
        return response

    def get_status(self, order_id) -> dict:
        params = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id,
        }
        response = self.get_response(self.url, params=params)

        status = response.get('status')
        response['status'] = self.statuses.get(status)
        return response


class GlobalApiClient(ApiClient):
    """
    Класс для клиента Api к GlobalSmm сервису.
    """
    errors = {
        'Not enough funds on balance': 'balance_error',
        'error.incorrect_service_id': 'id_error',
        'You have active order with this link. Please wait until order being completed.': 'active_order_link'
    }
    statuses = {
        'Partial': 'processing',
        'In progress': 'processing',
        'Pending': 'processing',
        'Completed': 'completed',
        'Canceled': 'canceled',
    }

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

        if order_id:
            response['success'] = True
        else:
            response['success'] = False
            error = response.get('error')
            response['error'] = self.errors.get(error, 'not_known')
        return response

    def get_status(self, order_id):
        params = {
            'key': self.api_key,
            'action': 'status',
            'order': order_id,
        }
        response = self.get_response(self.url, params=params)
        status = response.get('status', False)

        response['status'] = self.statuses.get(status)
        return response

    # def get_multiple_status(self, *order_ids) -> dict:
    #     data_of_orders = dict()
    #     for order_id in order_ids:
    #         status = self.get_status(order_id)
    #         data_of_orders[order_id] = status
    #         time.sleep(3)

    #     return data_of_orders
