from django.urls import reverse
import pytest


@pytest.mark.parametrize(['data', 'expected'],
    [
    (dict(thema='testhema', question='testquestion', notes='testnotes'), 200),
    (dict(header='', description=''), 200),
    ]
)
def test_auth_post_form(auth_client, data, expected):
    url = reverse('create_support_mail')
    response = auth_client.post(url, data)

    assert response.status_code == expected


def test_not_auth_get(client):
    response = client.get(reverse('create_support_mail'))

    assert response.status_code == 302


def test_auth_get(auth_client):
    response = auth_client.get(reverse('create_support_mail'))

    assert response.status_code == 200
