from django.urls import reverse
import pytest


@pytest.mark.parametrize(['data', 'expected'],
    [
    (dict(username='testuser', password='testpassword', confirm_password='testpassword', email='testmail'), 302),
    (dict(username='testuser', password='testpassword', confirm_password='testpassDord', email='testmail'), 200),
    (dict(username='$#%#@', password='#$@%#', confirm_password='#$@%#', email='#$@%#'), 200)
    ]
)
def test_not_auth_post_form(client, data, expected):
    url = reverse('sign_up')
    response = client.post(url, data)

    assert response.status_code == expected


def test_not_auth_get(client):
    response = client.get(reverse('sign_up'))

    assert response.status_code == 200


def test_not_auth_get(client):
    response = client.get(reverse('user_created'))

    assert response.status_code == 200