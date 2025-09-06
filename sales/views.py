from MBP.views import ProtectedModelViewSet
from .models import Customer, SalesOrder, SalesOrderItem, SalesPayment, SalesShipment, SalesInvoice
from .serializers import (
    CustomerSerializer, SalesOrderSerializer, SalesOrderItemSerializer,
    PaymentSerializer, ShipmentSerializer, InvoiceSerializer
)


# ------------------ Customer ------------------
class CustomerViewSet(ProtectedModelViewSet):
    queryset = Customer.objects.all().order_by("-created_at")
    serializer_class = CustomerSerializer
    model_name = "Customer"
    lookup_field = "slug"


# ------------------ SalesOrder ------------------
class SalesOrderViewSet(ProtectedModelViewSet):
    queryset = SalesOrder.objects.select_related("customer").all().order_by("-order_date")
    serializer_class = SalesOrderSerializer
    model_name = "SalesOrder"
    lookup_field = "slug"


# ------------------ SalesOrderItem ------------------
class SalesOrderItemViewSet(ProtectedModelViewSet):
    queryset = SalesOrderItem.objects.select_related("order", "product").all()
    serializer_class = SalesOrderItemSerializer
    model_name = "SalesOrderItem"
    lookup_field = "id"


# ------------------ Payment ------------------
class PaymentViewSet(ProtectedModelViewSet):
    queryset = SalesPayment.objects.select_related("order").all().order_by("-payment_date")
    serializer_class = PaymentSerializer
    model_name = "SalesPayment"
    lookup_field = "slug"


# ------------------ Shipment ------------------
class ShipmentViewSet(ProtectedModelViewSet):
    queryset = SalesShipment.objects.select_related("order", "warehouse").all()
    serializer_class = ShipmentSerializer
    model_name = "SalesShipment"
    lookup_field = "tracking_number"


# ------------------ Invoice ------------------
class InvoiceViewSet(ProtectedModelViewSet):
    queryset = SalesInvoice.objects.select_related("order").all().order_by("-invoice_date")
    serializer_class = InvoiceSerializer
    model_name = "SalesInvoice"
    lookup_field = "slug"
