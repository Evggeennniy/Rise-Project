from django.urls import reverse
import pytest


@pytest.mark.parametrize(['data', 'expected'],
    [
    (dict(username='testuser', password='testpassword'), 200),
    (dict(username='', password=''), 200),
    ]
)
def test_not_auth_post_form(client, data, expected):
    url = reverse('login')
    response = client.post(url, data)

    assert response.status_code == expected
