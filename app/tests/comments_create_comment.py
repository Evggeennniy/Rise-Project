from django.urls import reverse
import pytest


@pytest.mark.parametrize(['data', 'expected'],
    [
    (dict(comment='testcomment', rating=5), 302),
    (dict(comment='', rating=0), 200),
    ]
)
def test_auth_post_form(auth_client, data, expected):
    url = reverse('create_comment')

    response = auth_client.post(url, data)

    assert response.status_code == expected


def test_not_auth_get(client):
    response = client.get(reverse('create_comment'))

    assert response.status_code == 302


def test_auth_get(auth_client):
    response = auth_client.get(reverse('create_comment'))

    assert response.status_code == 200
