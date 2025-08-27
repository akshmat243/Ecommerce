from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRoleViewSet, LogoutView, LoginView, RegisterView, AddressViewSet, UserProfileViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', LoginView.as_view(), name='login'),
]


# Create user via POST /api/users/

# Update user via PUT/PATCH /api/users/{id}/

