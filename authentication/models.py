import uuid

from django.db import models

from abstarct_model.base_model import BaseModel
from .utils import generate_otp_code


class User(BaseModel):
    username = models.CharField(max_length=125, verbose_name='Имя пользователя')
    password = models.CharField(max_length=125, verbose_name='Пороль')
    email = models.CharField(max_length=125, verbose_name='Электронная почта')

    first_name = models.CharField(max_length=125, verbose_name='Имя', null=True, blank=True)
    last_name = models.CharField(max_length=125, verbose_name='Фамилия', null=True, blank=True)

    is_verified = models.BooleanField(default=False, verbose_name='Проверено')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['-created_at']


class OTP(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField(default=generate_otp_code,)
    otp_key = models.UUIDField(default=uuid.uuid4)

    attempts = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {str(self.otp_code)}"
