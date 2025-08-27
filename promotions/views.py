from .models import Coupon, GiftCard, Promotion
from .serializers import CouponSerializer, GiftCardSerializer, PromotionSerializer
from MBP.views import ProtectedModelViewSet  # your custom base viewset


class CouponViewSet(ProtectedModelViewSet):
    queryset = Coupon.objects.all().order_by("-created_at")
    serializer_class = CouponSerializer
    model_name = "Coupon"
    lookup_field = "slug"


class GiftCardViewSet(ProtectedModelViewSet):
    queryset = GiftCard.objects.all().order_by("-created_at")
    serializer_class = GiftCardSerializer
    model_name = "GiftCard"
    lookup_field = "slug"


class PromotionViewSet(ProtectedModelViewSet):
    queryset = Promotion.objects.all().order_by("-created_at")
    serializer_class = PromotionSerializer
    model_name = "Promotion"
    lookup_field = "slug"
