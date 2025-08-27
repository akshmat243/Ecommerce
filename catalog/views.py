from MBP.views import ProtectedModelViewSet
from rest_framework import filters

from .models import (
    Attribute, AttributeValue, ProductAttribute,
    Variant, VariantAttribute, BundleItem, Product, Category, Brand
)
from .serializers import (
    AttributeSerializer, AttributeValueSerializer,
    ProductAttributeSerializer, VariantSerializer,
    VariantAttributeSerializer, BundleItemSerializer,
    ProductSerializer, CategorySerializer, BrandSerializer
)


# ------------------ Category ------------------
class CategoryViewSet(ProtectedModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    model_name = "Category"
    lookup_field = "slug"

# ------------------ Brand ------------------
class BrandViewSet(ProtectedModelViewSet):  
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    model_name = "Brand"
    lookup_field = "slug"
    
# ------------------ Product ------------------
class ProductViewSet(ProtectedModelViewSet):
    queryset = Product.objects.select_related("category", "brand").all().order_by("-created_at")
    serializer_class = ProductSerializer
    model_name = "Product"
    lookup_field = "slug" 

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "slug", "sku", "short_description", "description"]
    ordering_fields = ["created_at", "updated_at", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Query params for filtering
        status = self.request.query_params.get("status")
        category = self.request.query_params.get("category")
        brand = self.request.query_params.get("brand")
        is_active = self.request.query_params.get("is_active")

        if status:
            queryset = queryset.filter(status=status)

        if category:
            queryset = queryset.filter(category__id=category)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset

# ------------------ Attribute ------------------
class AttributeViewSet(ProtectedModelViewSet):
    queryset = Attribute.objects.all().order_by("name")
    serializer_class = AttributeSerializer
    model_name = "Attribute"
    lookup_field = "slug"


# ------------------ AttributeValue ------------------
class AttributeValueViewSet(ProtectedModelViewSet):
    queryset = AttributeValue.objects.select_related("attribute").all().order_by("value")
    serializer_class = AttributeValueSerializer
    model_name = "AttributeValue"
    lookup_field = "slug"


# ------------------ ProductAttribute ------------------
class ProductAttributeViewSet(ProtectedModelViewSet):
    queryset = ProductAttribute.objects.select_related("product", "attribute").all()
    serializer_class = ProductAttributeSerializer
    model_name = "ProductAttribute"
    lookup_field = "id"  # No slug in model → use ID


# ------------------ Variant ------------------
class VariantViewSet(ProtectedModelViewSet):
    queryset = Variant.objects.select_related("product").all().order_by("name")
    serializer_class = VariantSerializer
    model_name = "Variant"
    lookup_field = "slug"


# ------------------ VariantAttribute ------------------
class VariantAttributeViewSet(ProtectedModelViewSet):
    queryset = VariantAttribute.objects.select_related("variant", "attribute_value").all()
    serializer_class = VariantAttributeSerializer
    model_name = "VariantAttribute"
    lookup_field = "id"  # No slug → use ID


# ------------------ BundleItem ------------------
class BundleItemViewSet(ProtectedModelViewSet):
    queryset = BundleItem.objects.select_related("bundle", "product").all()
    serializer_class = BundleItemSerializer
    model_name = "BundleItem"
    lookup_field = "id"  # No slug → use ID