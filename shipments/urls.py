from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingMethodViewSet, ShipmentViewSet, ShippingAddressViewSet

router = DefaultRouter()
router.register(r"shipping-methods", ShippingMethodViewSet, basename="shipping-method")
router.register(r"shipping-addresses", ShippingAddressViewSet, basename="shipping-address")
router.register(r"shipments", ShipmentViewSet, basename="shipment")

urlpatterns = [
    path("api/", include(router.urls)),
]
