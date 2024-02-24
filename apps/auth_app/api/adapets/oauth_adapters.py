from base64 import b64encode

import requests
from apps.auth_app.api.adapets import oauth_settings

from apps.auth_app.api.adapets.oauth_interfaces import SocialAuthAbstract
from apps.auth_app.models import CustomUser


class GoogleAuth(SocialAuthAbstract):
    """Authorization via Google"""

    def __init__(self, code: str) -> None:
        super().__init__(code, oauth_settings.GOOGLE_CLIENT_ID, oauth_settings.GOOGLE_CLIENT_SECRET)

    def get_access_token(self) -> str:
        url = "https://oauth2.googleapis.com/token"
        data = (
            f"client_id={self.client_id}"
            f"&client_secret={self.client_secret}"
            f"&code={self.code}"
            f"&grant_type=authorization_code"
            f"&redirect_uri={oauth_settings.REDIRECT_URL}"
        )
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise ValueError(CustomUser.Text.OAUTH_CODE_INVALID)

    def get_user_info(self, access_token: str) -> (int, str):
        """
        get google user id and email
        :param access_token:
        :return: [user_id, user_email]
        """
        url = "https://www.googleapis.com/oauth2/v2/userinfo/"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("id"), response.json().get("email")
        else:
            raise ValueError(CustomUser.Text.OAUTH_TOKEN_EXPIRED)

