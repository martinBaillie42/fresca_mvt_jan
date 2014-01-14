from django.db import models
from django.contrib.auth.models import User

class UserExtension(models.Model):
    user = models.OneToOneField(User)
    gmail = models.CharField(max_length=200)
