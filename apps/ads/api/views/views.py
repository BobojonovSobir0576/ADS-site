from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.ads.models import *
from apps.ads.api.serializers.serializers import (
    CategoryListSerializers,
    CountryListSerializers, CityListSerializers,
    CategoryDetailSerializers
)
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)
from utils.swaggers import swagger_extend_schema
from utils.expected_fields import check_required_key


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_extend_schema(fields=[], description="Category", tags=[''])
    def get(self, request):
        queryset = Category.objects.all().order_by('-id')
        serializers = CategoryListSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ Category Post View """
    @swagger_extend_schema(fields=['name', 'subcategory', 'icon'], description="Category Post", tags=[''])
    def post(self, request):
        valid_fields = {'name', 'subcategory', 'icon'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CategoryListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """
    @swagger_extend_schema(fields=[], description="Category", tags=[''])
    def get(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        serializers = CategoryDetailSerializers(queryset, context={'request': request})
        return success_response(serializers.data)

    """ Category Put View """
    @swagger_extend_schema(fields=['name', 'subcategory', 'icon'], description="Category Put", tags=[''])
    def put(self, request, pk):
        valid_fields = {'name', 'subcategory', 'icon'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Category, pk=pk)
        serializers = CategoryListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ Category Delete View """
    @swagger_extend_schema(fields=[], description="Category Delete", tags=[''])
    def delete(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class CountryListView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_extend_schema(fields=[], description="Country", tags=[''])
    def get(self, request):
        queryset = Country.objects.all().order_by('-id')
        serializers = CountryListSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ Category Post View """
    @swagger_extend_schema(fields=['name'], description="Category Post", tags=[''])
    def post(self, request):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CountryListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CountryDetailView(APIView):
    permission_classes = [AllowAny]
    """ Country Get View """
    @swagger_extend_schema(fields=[], description="Country", tags=[''])
    def get(self, request, pk):
        queryset = get_object_or_404(Country, pk=pk)
        serializers = CountryListSerializers(queryset, context={'request': request})
        return success_response(serializers.data)

    """ Country Put View """
    @swagger_extend_schema(fields=['name'], description="Country Put", tags=[''])
    def put(self, request, pk):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Country, pk=pk)
        serializers = CountryListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ Country Delete View """
    @swagger_extend_schema(fields=[], description="Country Delete", tags=[''])
    def delete(self, request, pk):
        queryset = get_object_or_404(Country, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class CityListView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_extend_schema(fields=[], description="Country", tags=[''])
    def get(self, request):
        queryset = Country.objects.all().order_by('-id')
        serializers = CountryListSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ Category Post View """
    @swagger_extend_schema(fields=['name'], description="Category Post", tags=[''])
    def post(self, request):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CountryListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CityDetailViews(APIView):
    permission_classes = [AllowAny]
    """ City Get View """
    @swagger_extend_schema(fields=[], description="City", tags=[''])
    def get(self, request, pk):
        queryset = get_object_or_404(City, pk=pk)
        serializers = CityListSerializers(queryset, context={'request': request})
        return success_response(serializers.data)

    """ City Put View """
    @swagger_extend_schema(fields=['name'], description="City Put", tags=[''])
    def put(self, request, pk):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(City, pk=pk)
        serializers = CityListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ City Delete View """
    @swagger_extend_schema(fields=[], description="City Delete", tags=[''])
    def delete(self, request, pk):
        queryset = get_object_or_404(City, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")
