import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_sale(authenticated_api_client, customer):
    """
    Testa a criação de uma venda.
    """
    url = reverse('toy_store:sale-list')
    data = {
        'customer': customer.id,
        'value': 100.50,
        'total_amount': 100.50
    }
    response = authenticated_api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_list_sales(authenticated_api_client, sale):
    """
    Testa a listagem de vendas.
    :param authenticated_api_client:
    :param sale:
    :return:
    """
    url = reverse('toy_store:sale-list')
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    results = response.data.get('results', response.data)
    assert any(s['id'] == sale.id for s in results)


@pytest.mark.django_db
def test_retrieve_sale(authenticated_api_client, sale):
    """
    Testa a recuperação de uma venda específica.
    :param authenticated_api_client:
    :param sale:
    :return:
    """
    url = reverse('toy_store:sale-detail', args=[sale.id])
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == sale.id


@pytest.mark.django_db
def test_update_sale(authenticated_api_client, sale):
    """
    Testa a atualização de uma venda.
    :param authenticated_api_client:
    :param sale:
    :return:
    """
    url = reverse('toy_store:sale-detail', args=[sale.id])
    data = {'total_amount': 200.00}
    response = authenticated_api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert float(response.data['total_amount']) == 200.00


@pytest.mark.django_db
def test_delete_sale(authenticated_api_client, sale):
    """
    Testa a exclusão de uma venda.
    :param authenticated_api_client:
    :param sale:
    :return:
    """
    url = reverse('toy_store:sale-detail', args=[sale.id])
    response = authenticated_api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_create_sale_missing_required_field(authenticated_api_client):
    """
    Testa a criação de uma venda sem o campo obrigatório 'customer'.
    :param authenticated_api_client:
    :return:
    """
    url = reverse('toy_store:sale-list')
    data = {
        # 'customer' está ausente
        'total_amount': 100.50
    }
    response = authenticated_api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'customer' in response.data


@pytest.mark.django_db
def test_list_sales_pagination(authenticated_api_client, sale):
    """
    Testa a paginação na listagem de vendas.
    :param authenticated_api_client:
    :param sale:
    :return:
    """
    from toy_store.models import Sale
    # Cria vendas extras para garantir mais de uma página
    for _ in range(10):
        Sale.objects.create(customer=sale.customer, sale_date='2023-10-02', total_amount=50)
    url = reverse('toy_store:sale-list')
    response = authenticated_api_client.get(url, {'page': 1, 'page_size': 5})
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert 'count' in response.data
    assert len(response.data['results']) == 10


@pytest.mark.django_db
def test_sale_permissions(api_client, sale):
    """
    Testa as permissões de acesso às vendas.
    :param api_client:
    :param sale:
    :return:
    """
    url = reverse('toy_store:sale-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    detail_url = reverse('toy_store:sale-detail', args=[sale.id])
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
