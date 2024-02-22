from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.ads.models import *
from apps.ads.api.serializers.serializers import (
    CategoryListSerializers,
    CountryListSerializers, CityListSerializers,
    OptionalFieldListSerializers, OptionalFieldThroughListSerializers,
    JobListSerializers, JobDetailSerializers, CategoryDetailSerializers
)
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)
from utils.swaggers import swagger_extend_schema
from utils.expected_fields import check_required_key
from utils.renderers import UserRenderers
from utils.pagination import PaginationMethod, StandardResultsSetPagination



