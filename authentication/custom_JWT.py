from rest_framework_simplejwt.authentication import JWTAuthentication
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from .models import User


class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_user(self, validated_token):
        user_id = validated_token['user_id']
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.UNAUTHORIZED)
        return user