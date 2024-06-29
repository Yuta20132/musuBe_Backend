from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=50)
    institution = models.CharField(max_length=255, null=True, blank=True)
    field_of_research = models.CharField(max_length=255, null=True, blank=True)