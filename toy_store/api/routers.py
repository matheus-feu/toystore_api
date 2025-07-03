from rest_framework.routers import DefaultRouter

from toy_store.api.viewsets import CustomerViewSet, SaleViewSet, SalesStatsViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'sales-stats', SalesStatsViewSet, basename='sales-stats')
