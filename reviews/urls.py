from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ProductReviewViewSet,
    ReviewCommentViewSet,
    ProductQuestionViewSet,
    ProductAnswerViewSet,
    ContentEngagementViewSet,
)

router = DefaultRouter()
router.register("reviews", ProductReviewViewSet, basename="productreview")
router.register("comments", ReviewCommentViewSet, basename="reviewcomment")
router.register("questions", ProductQuestionViewSet, basename="productquestion")
router.register("answers", ProductAnswerViewSet, basename="productanswer")
router.register("engagements", ContentEngagementViewSet, basename="contentengagement")

urlpatterns = [
    path("api/", include(router.urls)),
]
