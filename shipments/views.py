from .models import ShippingMethod, Shipment, ShippingAddress
from .serializers import ShippingMethodSerializer, ShipmentSerializer, ShippingAddressSerializer
from MBP.views import ProtectedModelViewSet


class ShippingMethodViewSet(ProtectedModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
    model_name = "ShippingMethod"
    lookup_field = "slug"


class ShippingAddressViewSet(ProtectedModelViewSet):
    queryset = ShippingAddress.objects.select_related("user").all()
    serializer_class = ShippingAddressSerializer
    model_name = "ShippingAddress"
    lookup_field = "id"   # UUID instead of slug


class ShipmentViewSet(ProtectedModelViewSet):
    queryset = Shipment.objects.select_related("order", "shipping_method").all()
    serializer_class = ShipmentSerializer
    model_name = "Shipment"
    lookup_field = "id"   # UUID instead of slug
