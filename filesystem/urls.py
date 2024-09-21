from django.urls import include, path
from rest_framework.routers import DefaultRouter

from filesystem import views as filesystem_views

router = DefaultRouter()
router.register(r"files", filesystem_views.FileView, basename="files")
router.register(r"images", filesystem_views.ImageView, basename="images")

urlpatterns = [
    path("", include(router.urls)),
]
