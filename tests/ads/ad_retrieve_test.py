import pytest

from ads.serializers import AdSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_retrieve(client, user_token):
    ad = AdFactory.create()
    expected_response = AdSerializer(ad).data

    response = client.get(
        f"/ad/{ad.pk}/",
        HTTP_AUTHORIZATION="Bearer " + user_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
