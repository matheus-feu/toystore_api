from decimal import Decimal

from django.db.models import Sum, Count
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from toy_store.api.serializers import (
    CustomerSerializer,
    SaleSerializer,
    SalesPerDaySerializer,
    CustomerHighlightSerializer
)
from toy_store.filters import CustomerFilterClass
from toy_store.models.customer import Customer
from toy_store.models.sale import Sale


@extend_schema(tags=['Customer'])
class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    rql_filter_class = CustomerFilterClass
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=['Sale'])
class SaleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing sale instances.
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        customer = Customer.objects.get(email=self.request.user.email)
        serializer.save(customer=customer)


@extend_schema(tags=['Stats'])
class SalesStatsViewSet(viewsets.GenericViewSet):
    """
    ViewSet para estatísticas de vendas.
    """
    queryset = Sale.objects.all()
    serializer_class = SalesPerDaySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='stats-per-day')
    def stats_per_day(self, request):
        """
        Retorna estatísticas de vendas por dia.
        """
        sales_per_day = (
            Sale.objects
            .values('sale_date')
            .annotate(total=Sum('total_amount'))
            .order_by('sale_date')
        )
        serializer = self.get_serializer(sales_per_day, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='highlights')
    def highlights(self, request):
        """
        Retorna os clientes com:
        - Maior volume de vendas (soma total)
        - Maior média por venda
        - Maior frequência de compra (dias únicos com vendas)
        """

        def build_entry(entry, value_field, value_format="{:.2f}"):
            if not entry:
                return {"customer_id": None, "customer_name": None, "value": None}
            value = entry[value_field]
            if isinstance(value, (float, Decimal)):
                value = float(value)
                value = value_format.format(value)
            return {
                "customer_id": entry["customer__id"],
                "customer_name": entry["customer__name"],
                "value": value,
            }

        top_volume = (
            Sale.objects.values('customer__id', 'customer__name')
            .annotate(total=Sum('total_amount'))
            .order_by('-total')
            .first()
        )

        top_avg = (
            Sale.objects.values('customer__id', 'customer__name')
            .annotate(avg=Sum('total_amount') / Count('id'))
            .order_by('-avg')
            .first()
        )

        top_days = (
            Sale.objects.values('customer__id', 'customer__name')
            .annotate(days=Count('sale_date', distinct=True))
            .order_by('-days')
            .first()
        )

        return Response({
            "top_sales_volume": CustomerHighlightSerializer(build_entry(top_volume, "total")).data,
            "top_average_sale": CustomerHighlightSerializer(build_entry(top_avg, "avg")).data,
            "top_unique_sale_days": CustomerHighlightSerializer(build_entry(top_days, "days", value_format="{}")).data,
        })
