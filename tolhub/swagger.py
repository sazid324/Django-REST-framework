from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get("tags", None) or getattr(
            self.view, "swagger_tags", []
        )
        if not tags:
            tags = [operation_keys[0]]

        return ["swagger_" + tag for tag in tags]
