from .models import SearchQuery, UserActivity, Recommendation
from .serializers import (
    SearchQuerySerializer,
    UserActivitySerializer,
    RecommendationSerializer,
)
from MBP.views import ProtectedModelViewSet  # assuming your base is here


class SearchQueryViewSet(ProtectedModelViewSet):
    queryset = SearchQuery.objects.select_related("user").all()
    serializer_class = SearchQuerySerializer
    model_name = "SearchQuery"
    lookup_field = "slug"


class UserActivityViewSet(ProtectedModelViewSet):
    queryset = UserActivity.objects.select_related("user", "product").all()
    serializer_class = UserActivitySerializer
    model_name = "UserActivity"
    lookup_field = "slug"


class RecommendationViewSet(ProtectedModelViewSet):
    queryset = Recommendation.objects.select_related("user", "product").all()
    serializer_class = RecommendationSerializer
    model_name = "Recommendation"
    lookup_field = "slug"
