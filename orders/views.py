from MBP.views import ProtectedModelViewSet
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from .models import Payment, Refund, Invoice
from .serializers import PaymentSerializer, RefundSerializer, InvoiceSerializer


class CartViewSet(ProtectedModelViewSet):
    queryset = Cart.objects.prefetch_related("items").all()
    serializer_class = CartSerializer
    model_name = "Cart"
    lookup_field = "slug"


class CartItemViewSet(ProtectedModelViewSet):
    queryset = CartItem.objects.select_related("cart", "product", "variant").all()
    serializer_class = CartItemSerializer
    model_name = "CartItem"
    lookup_field = "slug"


class OrderViewSet(ProtectedModelViewSet):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer
    model_name = "Order"
    lookup_field = "slug"


class OrderItemViewSet(ProtectedModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer
    model_name = "OrderItem"
    lookup_field = "slug"



class PaymentViewSet(ProtectedModelViewSet):
    queryset = Payment.objects.select_related("order", "user").all()
    serializer_class = PaymentSerializer
    model_name = "Payment"
    lookup_field = "slug"


class RefundViewSet(ProtectedModelViewSet):
    queryset = Refund.objects.select_related("payment").all()
    serializer_class = RefundSerializer
    model_name = "Refund"
    lookup_field = "slug"


class InvoiceViewSet(ProtectedModelViewSet):
    queryset = Invoice.objects.select_related("order").all()
    serializer_class = InvoiceSerializer
    model_name = "Invoice"
    lookup_field = "slug"
