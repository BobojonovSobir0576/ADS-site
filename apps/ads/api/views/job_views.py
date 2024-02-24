from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
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
from utils.expected_fields import check_required_key
from utils.renderers import UserRenderers
from utils.pagination import PaginationMethod, StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class JobListView(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderers]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "job_category",
        "title",
        "category",
        "city"
    ]

    job_category_param = openapi.Parameter('job_category', openapi.IN_QUERY, description="Filter by job category",
                                           type=openapi.TYPE_STRING)
    title_param = openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING)
    category_param = openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category",
                                       type=openapi.TYPE_STRING)
    city_param = openapi.Parameter('city', openapi.IN_QUERY, description="Filter by city", type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[job_category_param, title_param, category_param, city_param],
                         operation_description="Retrieve a list of jobs",
                         tags=['Ads'],
                         responses={200: JobListSerializers(many=True)})
    def get(self, request):
        queryset = Job.objects.select_related('user').filter(user=request.user).order_by('-id')
        queryset = self.filter_by_title(queryset, request)
        queryset = self.filter_by_category(queryset, request)
        queryset = self.filter_by_city(queryset, request)
        serializers = super().page(queryset, JobDetailSerializers, request)
        return success_response(serializers.data)

    def filter_by_title(self, queryset, request):
        title = request.query_params.get("title", '')
        if title:
            queryset = queryset.filter(
                Q(company__title__icontains=title)
            )
        return queryset

    def filter_by_category(self, queryset, request):
        category = request.query_params.get("category", [])
        if category:
            ids_category = [int(id_str) for id_str in category.split(",")]
            queryset = queryset.filter(Q(job_category__in=ids_category))
        return queryset

    def filter_by_city(self, queryset, request):
        city = request.query_params.get("city", [])
        if city:
            ids_city = [int(id_str) for id_str in city.split(",")]
            queryset = queryset.filter(Q(job_city__in=ids_city))
        return queryset

    @swagger_auto_schema(request_body=JobListSerializers,
                         operation_description="Ads Create",
                         tags=['Ads'],
                         responses={201: JobListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'title', 'category', 'city', 'description', 'contact_number', 'email', 'name',
                                   'user', 'status', 'photo', 'date_create', 'date_update', 'is_top', 'is_vip', 'additionally'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = JobListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)


