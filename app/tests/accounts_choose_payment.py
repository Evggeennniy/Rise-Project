from django.urls import reverse
import pytest


@pytest.mark.parametrize(['data', 'expected'],
    [
    (dict(fonds='UAH', value=20000), 302),
    (dict(fonds='USD', value=20000), 302),
    (dict(fonds='EUR', value=20000), 302),
    (dict(fonds='FAIL', value=20000), 200)
    ]
)
def test_auth_post_form(auth_client, data, expected):
    url = reverse('choose_payment')
    response = auth_client.post(url, data)

    assert response.status_code == expected


def test_not_auth_get(client):
    response = client.get(reverse('choose_payment'))

    assert response.status_code == 302


def test_auth_get(auth_client):
    response = auth_client.get(reverse('choose_payment'))

    assert response.status_code == 200
