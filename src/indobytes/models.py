from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150, default='', blank=True, null=True)
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    token_no = models.CharField(max_length=20, default='', blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
