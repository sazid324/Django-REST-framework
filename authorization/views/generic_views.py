from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from authorization import models as authorization_models
from authorization import permissions as authorization_permissions
from filesystem import models as filesystem_models


class ProfileView(viewsets.ModelViewSet):
    queryset = authorization_models.CustomUserModel.objects.all()
    serializer_class = None
    http_method_names = ["get", "put", "delete"]
    authentication_classes = [
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = None
    profile_type = None  # Type of user

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [
                permissions.IsAuthenticated,
                authorization_permissions.AdminPermission
            ]
        if self.action == "retrieve":
            self.permission_classes = [
                permissions.IsAuthenticated,
                authorization_permissions.AdminOrSelf,
            ]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return authorization_models.CustomUserModel.objects.none()
        if self.action == "list":
            if user.is_admin:
                return authorization_models.CustomUserModel.objects.filter(
                    user_type=self.profile_type
                )
            else:
                self.permission_denied(
                    self.request, message="Not authorized to view this list"
                )
        if self.action == "retrieve":
            if str(user.user_id) == str(self.kwargs.get("pk")):
                return authorization_models.CustomUserModel.objects.filter(
                    user_id=self.kwargs.get("pk"), user_type=self.profile_type
                )
            elif user.is_admin:
                return authorization_models.CustomUserModel.objects.filter(
                    user_id=self.kwargs.get("pk"), user_type=self.profile_type
                )
            else:
                self.permission_denied(
                    self.request, message="Not authorized to view this profile"
                )
        return authorization_models.CustomUserModel.objects.filter(user_id=user.user_id, user_type=self.profile_type)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        image_url = None
        if instance.image:
            image_instance = get_object_or_404(
                filesystem_models.ImageModel, pk=instance.image_id
            )
            image_url = image_instance.image.url if image_instance.image else None

        serializer = self.get_serializer(instance)

        response_data = serializer.data
        response_data.update({"image": image_url})
        return Response(response_data, status=status.HTTP_200_OK)
