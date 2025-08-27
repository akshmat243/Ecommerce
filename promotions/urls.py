from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, GiftCardViewSet, PromotionViewSet

router = DefaultRouter()
router.register("coupons", CouponViewSet, basename="coupon")
router.register("giftcards", GiftCardViewSet, basename="giftcard")
router.register("promotions", PromotionViewSet, basename="promotion")

urlpatterns = [
    path("api/", include(router.urls)),
]
