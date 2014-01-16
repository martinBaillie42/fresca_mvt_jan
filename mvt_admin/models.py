from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gmail = models.CharField(max_length=200)

    def __unicode__(self):
        return self.gmail

## below code ensures that the gmail field is created when a user is saved
# http://igorsobreira.com/2010/12/11/extending-user-model-in-django.html
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
## end of gmail field code

# row/object based permission granted in admin.py
class Domain(models.Model):
    name = models.CharField(max_length=200)
    user = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    UNPUBLISHED = 'unpublished'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (UNPUBLISHED, UNPUBLISHED),
        (PUBLISHED, PUBLISHED),
    )

    MVT = 'mvt'
    AB = 'ab'
    EXPERIMENT_TYPE_CHOICES = (
        (MVT, MVT),
        (AB, AB),
    )

    domain_id = models.ForeignKey(Domain)
    experiment_type = models.CharField(max_length=20, choices=EXPERIMENT_TYPE_CHOICES, default=MVT)
    name = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNPUBLISHED)
    uri = models.CharField(max_length=200)
    page_type = models.CharField(max_length=200)
    page_identifier = models.CharField(max_length=200)
    experiment_js = models.TextField(max_length=200, default='')

    def __unicode__(self):
        return self.name

class Variant(models.Model):
    experiment_id = models.ForeignKey(Domain)
    number = models.IntegerField()
    variant_js = models.TextField(max_length=200, default='')

    def __unicode__(self):
        return self.number