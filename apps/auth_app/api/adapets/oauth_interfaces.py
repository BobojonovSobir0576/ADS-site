from abc import ABC, abstractmethod


class SocialAuthAbstract(ABC):
    """Abstract class for authorization via social media. networks"""

    def __init__(self, code: str, client_id: str, client_secret: str) -> None:
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret

    def set_api_keys(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    def get_access_token(self) -> str:
        """Returns access_token"""
        raise NotImplementedError

    @abstractmethod
    def get_user_info(self, access_token: str) -> (int, str):
        """Returns the user_id and email of the user"""
        raise NotImplementedError

    def auth(self) -> (int, str):
        """Returns the user_id and email of the user"""

        access_token = self.get_access_token()
        social_user_id, social_user_email = self.get_user_info(access_token)
        return social_user_id, social_user_email
