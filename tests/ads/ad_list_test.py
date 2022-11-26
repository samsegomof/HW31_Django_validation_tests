import pytest
from django.urls import reverse
from rest_framework import status

from ads.serializers import AdSerializer
from tests.factories.ad import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    url = reverse('all_ads')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
