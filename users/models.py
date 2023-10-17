
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    is_active = models.BooleanField(default=True)

    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.UUIDField(default=uuid.uuid4, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
