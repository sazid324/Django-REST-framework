from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from . import models


class ItemAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


admin.site.register(models.FileModel)
admin.site.register(models.ImageModel, ItemAdmin)
