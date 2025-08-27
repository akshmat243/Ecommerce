from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarehouseViewSet,
    StockViewSet,
    ProductPriceViewSet,
    StockTransactionViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'product-prices', ProductPriceViewSet, basename='productprice')
router.register(r'stock-transactions', StockTransactionViewSet, basename='stocktransaction')

urlpatterns = [
    path('api/', include(router.urls)),
]
