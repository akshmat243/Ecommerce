from MBP.views import ProtectedModelViewSet
from .models import Warehouse, Stock, ProductPrice, StockTransaction
from .serializers import WarehouseSerializer, StockSerializer, ProductPriceSerializer, StockTransactionSerializer


# ------------------ Warehouse ------------------
class WarehouseViewSet(ProtectedModelViewSet):
    queryset = Warehouse.objects.all().order_by("name")
    serializer_class = WarehouseSerializer
    model_name = "Warehouse"
    lookup_field = "slug"


# ------------------ Stock ------------------
class StockViewSet(ProtectedModelViewSet):
    queryset = Stock.objects.select_related("product", "variant", "warehouse").all()
    serializer_class = StockSerializer
    model_name = "Stock"
    lookup_field = "id"  # Use ID since Stock does not have slug


# ------------------ ProductPrice ------------------
class ProductPriceViewSet(ProtectedModelViewSet):
    queryset = ProductPrice.objects.select_related("product", "variant", "warehouse").all()
    serializer_class = ProductPriceSerializer
    model_name = "ProductPrice"
    lookup_field = "id"  # Use ID since ProductPrice does not have slug


# ------------------ StockTransaction ------------------
class StockTransactionViewSet(ProtectedModelViewSet):
    queryset = StockTransaction.objects.select_related("stock").all().order_by("-created_at")
    serializer_class = StockTransactionSerializer
    model_name = "StockTransaction"
    lookup_field = "id"  # Use ID since StockTransaction does not have slug
