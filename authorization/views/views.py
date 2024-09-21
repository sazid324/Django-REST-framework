from rest_framework import authentication, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from authorization import choices as authorization_choices
from authorization import models as authorization_models
from authorization import permissions as authorization_permissions
from authorization import serializers as authentication_serializers
from authorization import serializers as authorization_serializers
from authorization.views import generic_views as authorization_generic_views


class UserProfileView(authorization_generic_views.ProfileView):
    serializer_class = authentication_serializers.UserProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        authorization_permissions.UserPermission,
    ]
    profile_type = authorization_choices.UserChoices.USER
    swagger_tags = ["authorization_user"]


class AdminProfileView(authorization_generic_views.ProfileView):
    serializer_class = authentication_serializers.AdminProfileSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        authorization_permissions.AdminPermission,
    ]
    profile_type = authorization_choices.UserChoices.ADMIN
    swagger_tags = ["authorization_admin"]


class ProfileManagementView(generics.UpdateAPIView):
    queryset = authorization_models.CustomUserModel.objects.all()
    serializer_class = authorization_serializers.ProfileManagementSerializer
    http_method_names = ["put"]
    authentication_classes = [
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
        authorization_permissions.AdminPermission,
    ]
    swagger_tags = ["authorization_admin"]


class AddressView(viewsets.ModelViewSet):
    queryset = authorization_models.AddressModel.objects.all()
    serializer_class = authentication_serializers.AddressSerializer
    http_method_names = ["get", "post", "put", "delete"]
    authentication_classes = [
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ["authorization_address"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return authorization_models.AddressModel.objects.none()
        return authorization_models.AddressModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
