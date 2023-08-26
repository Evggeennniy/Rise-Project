from django.urls import reverse


def test_not_auth_get(client):
    response = client.get(reverse('support_mails'))

    assert response.status_code == 302


def test_auth_get(auth_client):
    response = auth_client.get(reverse('support_mails'))

    assert response.status_code == 200