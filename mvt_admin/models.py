from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

class UserExtension(models.Model):
    user = models.OneToOneField(User)
    gmail = models.CharField(max_length=200)

# below code ensures that the gmail field is created when a user is saved
# http://igorsobreira.com/2010/12/11/extending-user-model-in-django.html
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)