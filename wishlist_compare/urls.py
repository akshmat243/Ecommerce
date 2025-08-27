from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistViewSet, WishlistItemViewSet, CompareListViewSet, CompareItemViewSet

router = DefaultRouter()
router.register(r"wishlists", WishlistViewSet, basename="wishlist")
router.register(r"wishlist-items", WishlistItemViewSet, basename="wishlist-item")
router.register(r"compare-lists", CompareListViewSet, basename="compare-list")
router.register(r"compare-items", CompareItemViewSet, basename="compare-item")

urlpatterns = [
    path("api/", include(router.urls)),
]
