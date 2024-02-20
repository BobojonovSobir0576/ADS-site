from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.generics import GenericAPIView
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework import status
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from apps.auth_app.api.serializers.serializers import GoogleSocialAuthSerializer
from apps.auth_app.models import CustomUser
from allauth.account.views import SignupView
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth.models import Group


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
