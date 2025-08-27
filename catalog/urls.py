from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttributeViewSet, AttributeValueViewSet,
    ProductAttributeViewSet, VariantViewSet,
    VariantAttributeViewSet, BundleItemViewSet,
    ProductViewSet, CategoryViewSet, BrandViewSet
)

router = DefaultRouter()

# Register endpoints
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'brands', BrandViewSet, basename="brand")
router.register(r'products', ProductViewSet, basename="product")
router.register(r'attributes', AttributeViewSet, basename="attribute")
router.register(r'attribute-values', AttributeValueViewSet, basename="attributevalue")
router.register(r'product-attributes', ProductAttributeViewSet, basename="productattribute")
router.register(r'variants', VariantViewSet, basename="variant")
router.register(r'variant-attributes', VariantAttributeViewSet, basename="variantattribute")
router.register(r'bundle-items', BundleItemViewSet, basename="bundleitem")

urlpatterns = [
    path('api/', include(router.urls)),
]
