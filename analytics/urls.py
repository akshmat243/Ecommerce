from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchQueryViewSet, UserActivityViewSet, RecommendationViewSet

router = DefaultRouter()
router.register(r"search-queries", SearchQueryViewSet, basename="searchquery")
router.register(r"user-activities", UserActivityViewSet, basename="useractivity")
router.register(r"recommendations", RecommendationViewSet, basename="recommendation")

urlpatterns = [
    path("api/", include(router.urls)),
]
