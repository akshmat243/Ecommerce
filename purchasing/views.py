from MBP.views import ProtectedModelViewSet
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceipt
from .serializers import SupplierSerializer, PurchaseOrderSerializer, PurchaseOrderItemSerializer, GoodsReceiptSerializer

# ---------------- Supplier ----------------
class SupplierViewSet(ProtectedModelViewSet):
    queryset = Supplier.objects.all().order_by('name')
    serializer_class = SupplierSerializer
    model_name = "Supplier"
    lookup_field = "slug"


# ---------------- PurchaseOrder ----------------
class PurchaseOrderViewSet(ProtectedModelViewSet):
    queryset = PurchaseOrder.objects.select_related('supplier', 'warehouse').all().order_by('-order_date')
    serializer_class = PurchaseOrderSerializer
    model_name = "PurchaseOrder"
    lookup_field = "slug"


# ---------------- PurchaseOrderItem ----------------
class PurchaseOrderItemViewSet(ProtectedModelViewSet):
    queryset = PurchaseOrderItem.objects.select_related('product', 'variant', 'purchase_order').all()
    serializer_class = PurchaseOrderItemSerializer
    model_name = "PurchaseOrderItem"
    lookup_field = "id"  # Use ID since no slug field


class GoodsReceiptViewSet(ProtectedModelViewSet):
    queryset = GoodsReceipt.objects.select_related("purchase_order").all().order_by("-created_at")
    serializer_class = GoodsReceiptSerializer
    model_name = "GoodsReceipt"
    lookup_field = "slug"
