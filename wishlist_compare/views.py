from .models import Wishlist, WishlistItem, CompareList, CompareItem
from .serializers import (
    WishlistSerializer,
    WishlistItemSerializer,
    CompareListSerializer,
    CompareItemSerializer,
)
from MBP.views import ProtectedModelViewSet  # adjust import path as per your project


class WishlistViewSet(ProtectedModelViewSet):
    queryset = Wishlist.objects.select_related("user").prefetch_related("items__product")
    serializer_class = WishlistSerializer
    model_name = "Wishlist"
    lookup_field = "slug"

    def get_queryset(self):
        # Only return wishlists of the current user
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistItemViewSet(ProtectedModelViewSet):
    queryset = WishlistItem.objects.select_related("wishlist", "product")
    serializer_class = WishlistItemSerializer
    model_name = "WishlistItem"

    def get_queryset(self):
        return super().get_queryset().filter(wishlist__user=self.request.user)

    def perform_create(self, serializer):
        wishlist_slug = self.request.data.get("wishlist_slug")
        wishlist = Wishlist.objects.get(user=self.request.user, slug=wishlist_slug)
        serializer.save(wishlist=wishlist)


class CompareListViewSet(ProtectedModelViewSet):
    queryset = CompareList.objects.select_related("user").prefetch_related("items__product")
    serializer_class = CompareListSerializer
    model_name = "CompareList"
    lookup_field = "slug"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure each user has only one CompareList
        compare_list, _ = CompareList.objects.get_or_create(user=self.request.user)
        return compare_list


class CompareItemViewSet(ProtectedModelViewSet):
    queryset = CompareItem.objects.select_related("compare_list", "product")
    serializer_class = CompareItemSerializer
    model_name = "CompareItem"

    def get_queryset(self):
        return super().get_queryset().filter(compare_list__user=self.request.user)

    def perform_create(self, serializer):
        compare_list, _ = CompareList.objects.get_or_create(user=self.request.user)
        serializer.save(compare_list=compare_list)
