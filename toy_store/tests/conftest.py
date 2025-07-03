import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from toy_store.models import Sale, Customer


@pytest.fixture
def user(db):
    """
    Fixture to create a test admin user.
    :param db:
    :return:
    """
    from django.contrib.auth.models import User
    return User.objects.create_user(username="admin", password="admin123")


@pytest.fixture
def api_client(user):
    """
    Fixture to create an API client and log in as the admin user.
    :param user:
    :return:
    """
    client = APIClient()
    client.login(username="admin", password="admin123")
    return client


@pytest.fixture
def customer(db, user):
    """
    Fixture to create a test customer.
    :param db:
    :param user:
    :return:
    """
    from toy_store.models import Customer
    return Customer.objects.create(
        name='Cliente Teste',
        email=user.email,
        phone='12345678',
        address='Rua Teste, 123',
        date_of_birth='1990-01-01'
    )


@pytest.fixture
def sale(db, customer):
    """
    Fixture to create a test sale.
    :param db:
    :param customer:
    :return:
    """
    from toy_store.models import Sale
    return Sale.objects.create(
        customer=customer,
        sale_date='2023-10-01',
        total_amount=100.50
    )


@pytest.fixture
def customer_factory(db):
    def create_customer(**kwargs):
        return Customer.objects.create(**kwargs)

    return create_customer


@pytest.fixture
def sale_factory(db, customer_factory):
    def create_sale(**kwargs):
        if 'customer' not in kwargs:
            kwargs['customer'] = customer_factory(name='Cliente Padrão')
        return Sale.objects.create(**kwargs)

    return create_sale


@pytest.fixture
def authenticated_api_client(api_client, db):
    """
Fixture to create an authenticated API client.
    :param api_client:
    :param db:
    :return:
    """
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='admin', defaults={'password': 'admin123'})
    api_client.force_authenticate(user=user)
    return api_client
