from django.db import models
from sorl.thumbnail import ImageField as ThumbnailImageField

from tolhub.mixins.models import AuthorWithTimeStampMixin


class FileModel(AuthorWithTimeStampMixin):
    file = models.FileField(upload_to="files/%Y/%m/%d")


class ImageModel(AuthorWithTimeStampMixin):
    image = ThumbnailImageField(upload_to="images/%Y/%m/%d")
