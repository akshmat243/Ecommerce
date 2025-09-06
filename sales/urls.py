from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CustomerViewSet, SalesOrderViewSet, SalesOrderItemViewSet,
    PaymentViewSet, ShipmentViewSet, InvoiceViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'orders', SalesOrderViewSet, basename='salesorder')
router.register(r'order-items', SalesOrderItemViewSet, basename='salesorderitem')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'shipments', ShipmentViewSet, basename='shipment')
router.register(r'order-invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path("api/", include(router.urls)),
]
