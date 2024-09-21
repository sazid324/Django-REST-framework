import logging

from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from filesystem import models as filesystem_models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = filesystem_models.FileModel
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = filesystem_models.ImageModel
        fields = "__all__"

    def get_thumbnail(self, obj):
        try:
            thumbnail = get_thumbnail(obj.image, "x100", quality=99)
            return self.context["request"].build_absolute_uri(thumbnail.url)
        except Exception as e:
            logging.error(f"Failed to generate thumbnail. Error: {e}")
            return None
