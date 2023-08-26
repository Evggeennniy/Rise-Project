from django.urls import reverse


def test_not_auth_get(client):
    response = client.get(reverse('comments'))

    assert response.status_code == 200


def test_auth_get(auth_client):
    response = auth_client.get(reverse('create_comment'))

    assert response.status_code == 200