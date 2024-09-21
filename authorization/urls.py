from django.urls import include, path
from rest_framework import routers

from authorization.views import views as authorization_views

router = routers.DefaultRouter()
router.register(
    r"user-profile", authorization_views.UserProfileView, basename="user-profile"
)
router.register(
    r"admin-profile", authorization_views.AdminProfileView, basename="admin-profile"
)
router.register(r"address", authorization_views.AddressView, basename="address")

urlpatterns = [
    path(r"api/", include(router.urls)),
    path(
        "api/profile-management/<uuid:pk>/",
        authorization_views.ProfileManagementView.as_view(),
        name="profile-management",
    ),
]
