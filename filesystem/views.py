from rest_framework import authentication, parsers, permissions, viewsets
from rest_framework_simplejwt import authentication as jwt_authentication

from filesystem import models as filesystem_models
from filesystem import serializers as filesystem_serializers


class FileView(viewsets.ModelViewSet):
    queryset = filesystem_models.ImageModel.objects.all()
    serializer_class = filesystem_serializers.FileSerializer
    parser_classes = [parsers.MultiPartParser]
    authentication_classes = [
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ["files"]


class ImageView(viewsets.ModelViewSet):
    queryset = filesystem_models.ImageModel.objects.all()
    serializer_class = filesystem_serializers.ImageSerializer
    parser_classes = [parsers.MultiPartParser]
    authentication_classes = [
        jwt_authentication.JWTAuthentication,
        authentication.SessionAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]
    swagger_tags = ["images"]
