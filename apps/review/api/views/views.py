from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.review.models import *
from apps.review.api.serializers.serializers import (
    ReviewListSerializers,
    ReviewDetailSerializers
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


class ReviewListView(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderers]

    """ Review Get View """
    @swagger_extend_schema(fields=[], description="User Reviews Get", tags=[''])
    def get(self, request):
        try:
            queryset = Review.objects.select_related('user').filter(
                user=request.user
            )
        except ObjectDoesNotExist:
            return bad_request_response('Object Does Not Exist')

        serializer = super().page(queryset, ReviewDetailSerializers, request)
        return success_response(serializer.data)

    """ Review Post View """
    @swagger_extend_schema(fields=['job', 'rating', 'description', 'first_name', 'email'], description="Team Roles Create", tags=[''])
    def post(self, request):
        valid_fields = {'job', 'rating', 'description', 'first_name', 'email'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = ReviewListSerializers(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_created_response(serializer.data)
        return bad_request_response(serializer.errors)


class ReviewDetailsViews(APIView):
    permission_classes = [AllowAny]

    """ Review Get View """
    @swagger_extend_schema(fields=[], description="Review", tags=[''])
    def get(self, request, pk):
        queryset = get_object_or_404(Review, pk=pk)
        serializer = ReviewDetailSerializers(queryset)
        return success_response(serializer.data)

    """ Review Put View """
    @swagger_extend_schema(fields=['job', 'rating', 'description', 'first_name', 'email'], description="Review Update", tags=[''])
    def put(self, request, pk):
        valid_fields = {'job', 'rating', 'description', 'first_name', 'email'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Review, pk=pk)
        serializer = ReviewListSerializers(
            instance=queryset, data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    """ Review Delete View """
    @swagger_extend_schema(fields=[], description="Review Delete", tags=[''])
    def delete(self, request, pk):
        queryset = get_object_or_404(Review, pk=pk)
        queryset.delete()
        return success_deleted_response('Successfully deleted')
