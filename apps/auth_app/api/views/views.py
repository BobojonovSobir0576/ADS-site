from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from apps.auth_app.api.serializers.serializers import (
    RegisterSerializer,
    InformationSerializer,
    LoginSerializer, GoogleSocialAuthSerializer
)
from utils.expected_fields import check_required_key
from utils.renderers import UserRenderers
from utils.responses import bad_request_response, success_created_response, success_response, success_deleted_response
from utils.swaggers import swagger_extend_schema, swagger_schema
from utils.token import get_token_for_user


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


@swagger_extend_schema(fields={"first_name", "last_name", 'photo', 'about', 'phone', 'email'},
                       description="Register", tags=['Register'])
@swagger_schema(serializer=RegisterSerializer)
class RegisterViews(APIView):

    def post(self, request):
        valid_fields = {"first_name", "last_name", 'photo', 'about', 'phone', 'email', 'groups', 'password'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.instance
            token = get_token_for_user(user)
            return success_created_response(token)
        return bad_request_response(serializer.errors)


@swagger_extend_schema(fields={"phone", "password"}, description="Login", tags=['Login'])
@swagger_schema(serializer=LoginSerializer)
class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        expected_fields = {"phone", "password"}
        received_fields = set(request.data.keys())
        unexpected_fields = received_fields - expected_fields

        if unexpected_fields:
            return bad_request_response(
                f"Unexpected fields: {', '.join(unexpected_fields)}"
            )

        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = self.generate_user_token(user)

        return success_response(token)

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)

    def generate_user_token(self, user):
        return get_token_for_user(user)


@swagger_extend_schema(fields={"first_name", "last_name", 'photo', 'about', 'phone', 'email'}, description="Custom User Profile",
                       tags=['Profile'])
@swagger_schema(serializer=RegisterSerializer)
class ProfileViews(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]

    def get(self, request):
        serializer = InformationSerializer(request.user, context={'request': request} )
        return success_response(serializer.data)

    def put(self, request):
        valid_fields = {"first_name", "last_name", 'photo', 'about', 'phone', 'email'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = RegisterSerializer(request.user, data=request.data, partial=True,
                                              context={'avatar': request.FILES.get('avatar', None), 'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    def delete(self, request):
        request.user.delete()
        return success_deleted_response("User deleted")