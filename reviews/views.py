from .models import (
    ProductReview,
    ReviewComment,
    ProductQuestion,
    ProductAnswer,
    ContentEngagement,
)
from .serializers import (
    ProductReviewSerializer,
    ReviewCommentSerializer,
    ProductQuestionSerializer,
    ProductAnswerSerializer,
    ContentEngagementSerializer,
)
from MBP.views import ProtectedModelViewSet  # your base viewset


class ProductReviewViewSet(ProtectedModelViewSet):
    queryset = ProductReview.objects.select_related("product", "user").all()
    serializer_class = ProductReviewSerializer
    model_name = "ProductReview"
    lookup_field = "slug"


class ReviewCommentViewSet(ProtectedModelViewSet):
    queryset = ReviewComment.objects.select_related("review", "user").all()
    serializer_class = ReviewCommentSerializer
    model_name = "ReviewComment"
    lookup_field = "id"


class ProductQuestionViewSet(ProtectedModelViewSet):
    queryset = ProductQuestion.objects.select_related("product", "user").all()
    serializer_class = ProductQuestionSerializer
    model_name = "ProductQuestion"
    lookup_field = "id"


class ProductAnswerViewSet(ProtectedModelViewSet):
    queryset = ProductAnswer.objects.select_related("question", "user").all()
    serializer_class = ProductAnswerSerializer
    model_name = "ProductAnswer"
    lookup_field = "id"


class ContentEngagementViewSet(ProtectedModelViewSet):
    queryset = ContentEngagement.objects.select_related("user", "review", "comment", "answer").all()
    serializer_class = ContentEngagementSerializer
    model_name = "ContentEngagement"
    lookup_field = "id"
