from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter


def swagger_schema(serializer):
    return swagger_auto_schema(
        request_body=serializer,
        responses={200: serializer},
    )


def swagger_extend_schema(fields, description, tags: []):
    parameters = [
        OpenApiParameter(name=field, type=str)
        for field in fields
    ]
    return extend_schema(
        parameters=parameters, description=description, tags=tags
    )
