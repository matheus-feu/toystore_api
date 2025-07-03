import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_customer(authenticated_api_client):
    """
    Testa a criação de um cliente.
    :param authenticated_api_client:
    :return:
    """
    from toy_store.models import Customer
    url = reverse('toy_store:customer-list')
    data = {
        'name': 'Maria',
        'email': 'maria@email.com',
        'phone': '123456789',
        'address': 'Rua A, 123',
        'date_of_birth': '1990-01-01'
    }
    response = authenticated_api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Customer.objects.count() == 1
    assert Customer.objects.filter(email='maria@email.com').exists()


@pytest.mark.django_db
def test_list_customers(authenticated_api_client, customer):
    """
    Testa a listagem de clientes.
    :param authenticated_api_client:
    :param customer:
    :return:
    """
    url = reverse('toy_store:customer-list')
    response = authenticated_api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    # Se a resposta for paginada
    if "results" in response.data:
        results = response.data["results"]
    else:
        results = response.data
    assert any(c["email"] == customer.email for c in results)


@pytest.mark.django_db
def test_update_customer(authenticated_api_client, customer):
    """
    Testa a atualização de um cliente.
    :param authenticated_api_client:
    :param customer:
    :return:
    """
    url = reverse('toy_store:customer-detail', args=[customer.id])
    data = {
        'name': 'João Atualizado',
        'email': 'joao@email.com',
        'phone': '987654321',
        'address': 'Rua B, 456',
        'date_of_birth': '1992-02-02'
    }
    response = authenticated_api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.name == 'João Atualizado'


@pytest.mark.django_db
def test_delete_customer(authenticated_api_client, customer):
    """
    Testa a exclusão de um cliente.
    :param authenticated_api_client:
    :param customer:
    :return:
    """
    from toy_store.models import Customer
    url = reverse('toy_store:customer-detail', args=[customer.id])
    response = authenticated_api_client.delete(url, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Customer.objects.filter(id=customer.id).exists()


@pytest.mark.django_db
def test_get_customer(authenticated_api_client, customer):
    """
    Testa a recuperação de um cliente específico.
    :param authenticated_api_client:
    :param customer:
    :return:
    """
    url = reverse('toy_store:customer-detail', args=[customer.id])
    response = authenticated_api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == customer.name
    assert response.data['email'] == customer.email
    assert response.data['phone'] == customer.phone
    assert response.data['address'] == customer.address
    assert response.data['date_of_birth'] == str(customer.date_of_birth)


@pytest.mark.django_db
def test_get_non_existent_customer(authenticated_api_client):
    """
    Testa a recuperação de um cliente que não existe.
    :param authenticated_api_client:
    :return:
    """
    url = reverse('toy_store:customer-detail', args=[9999])
    response = authenticated_api_client.get(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_customer_invalid_date_of_birth(authenticated_api_client):
    """
    Testa a criação de um cliente com data de nascimento futura.
    :param authenticated_api_client:
    :return:
    """
    url = reverse('toy_store:customer-list')
    data = {
        'name': 'Nome Válido',
        'email': 'email@valido.com',
        'phone': '12345678',
        'address': 'Endereço válido',
        'date_of_birth': '2099-01-01'  # Data futura
    }
    response = authenticated_api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'date_of_birth' in response.data
