import pytest
from django.test import Client
from django.contrib.auth import get_user_model


@pytest.fixture
def auth_client():
    client = Client()
    username='testuser'
    password='testpassword'
    email = 'testemail'
    user = get_user_model().objects.create_user(username=username, password=password, email=email)

    client.login(username=username, password=password, email=email)
    return client


@pytest.fixture(autouse=True, scope='function')
def enable_db_access_for_all_tests(db):
    """
    Give access to database for all tests
    """
