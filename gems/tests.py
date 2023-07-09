from pathlib import Path

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse

from gems.urls import DEALS_VIEW_NAME

deals_path = reverse(DEALS_VIEW_NAME)
cwd = Path(__file__).parent

CUSTOMERS_COUNT_EMPTY = 0
CUSTOMERS_COUNT_FILLED = 5


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def client_data_filled(csv_file: Path, client: APIClient) -> APIClient:
    with csv_file.open('rb') as source_file:
        data = {'deals': source_file}
        client.post(deals_path, data, format='multipart')
    return client


@pytest.fixture
def csv_file() -> Path:
    return cwd / 'csv_data/deals.csv'


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('client_name', 'customers_count'),
    [
        ('client', CUSTOMERS_COUNT_EMPTY),
        ('client_data_filled', CUSTOMERS_COUNT_FILLED),
    ],
)
def test_customers_empty(
    client_name: str, customers_count: int, request: pytest.FixtureRequest
):
    client = request.getfixturevalue(client_name)
    response = client.get(deals_path, format='json')
    assert response.status_code == status.HTTP_200_OK, response.content

    result = response.json()

    assert 'response' in result
    assert len(result['response']) == customers_count


@pytest.mark.django_db
def test_upload_deals(csv_file: Path, client: APIClient):
    with csv_file.open('rb') as source_file:
        data = {'deals': source_file}
        response = client.post(deals_path, data, format='multipart')

    assert response.status_code == status.HTTP_200_OK

    result = response.json()

    assert 'Status' in result
    assert result['Status'] == 'OK'
