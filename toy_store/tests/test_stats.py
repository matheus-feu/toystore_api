import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_sales_stats_view(authenticated_api_client, sale_factory):
    """
    Testa a view de estatísticas de vendas por dia.
    Cria vendas em datas distintas e verifica se a resposta da API
    retorna corretamente as datas das vendas realizadas.
    """
    sale_factory(sale_date='2024-06-01', total_amount=100)
    sale_factory(sale_date='2024-06-01', total_amount=50)
    sale_factory(sale_date='2024-06-02', total_amount=200)
    url = reverse('sales-stats')
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    dates = [item['date'] for item in response.data]
    assert '2024-06-01' in dates
    assert '2024-06-02' in dates


@pytest.mark.django_db
def test_sales_highlights_view(authenticated_api_client, sale_factory, customer_factory):
    """
    Testa a view de destaques de vendas.
    Cria clientes e vendas com e-mails únicos e verifica se a resposta da API
    retorna corretamente os destaques de vendas, como maior volume, maior média e dias de maior venda.
    """
    c1 = customer_factory(name='Cliente 1', email='c1@email.com')
    c2 = customer_factory(name='Cliente 2', email='c2@email.com')
    sale_factory(customer=c1, sale_date='2024-06-01', total_amount=100)
    sale_factory(customer=c1, sale_date='2024-06-02', total_amount=200)
    sale_factory(customer=c2, sale_date='2024-06-01', total_amount=300)
    url = reverse('sales-highlights')
    response = authenticated_api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['top_volume'] is not None
    assert response.data['top_avg'] is not None
    assert response.data['top_days'] is not None
