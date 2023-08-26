from django.urls import reverse


def test_not_auth_get(client):
    response = client.get(reverse('services_category'))

    assert response.status_code == 200
