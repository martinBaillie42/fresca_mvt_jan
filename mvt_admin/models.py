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

    class Meta:
        permissions = (
            ('view_domain', 'Can view domain'),
        )

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

    domain = models.ForeignKey(Domain)
    experiment_type = models.CharField(max_length=20, choices=EXPERIMENT_TYPE_CHOICES, default=MVT)
    name = models.CharField(max_length=200)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=UNPUBLISHED)
    uri = models.CharField(max_length=200)
    page_type = models.CharField(max_length=200)
    page_identifier = models.CharField(max_length=200)
    experiment_js = models.TextField(max_length=200, default='')

    # really this is view tier stuff shouldn't be in the model?
    # also the link is hard coded. If it is mixined then needs to be dynamic
    def selflink(self):
        if self.id:
            return "<a href='http://localhost:8000/fresca_mvt_jan/admin/mvt_admin/experiment/%s' >Edit</a>" % str(self.id)
        else:
            return "Not present"

    selflink.allow_tags = True
    

    def __unicode__(self):
        return self.name

class Variant(models.Model):
    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    experiment = models.ForeignKey(Experiment)
    number = models.IntegerField()
    state = models.CharField(max_length=10, choices=STATE)

    # really this is view tier stuff shouldn't be in the model?
    # also the link is hard coded. If it is mixined then needs to be dynamic
    def selflink(self):
        if self.id:
            return "<a href='http://localhost:8000/fresca_mvt_jan/admin/mvt_admin/variant/%s' >Edit</a>" % str(self.id)
        else:
            return "Not present"

    selflink.allow_tags = True

    def __unicode__(self):
        return str(self.number)

class Element(models.Model):
    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    variant = models.ForeignKey(Variant)
    selector = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=10, choices=STATE)

    def natural_key(self):
        return self.selector


    def __unicode__(self):
        return str(self.selector)

class Declaration(models.Model):
    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    element = models.ForeignKey(Element)
    property = models.CharField(max_length=50, default='')
    value = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=10, choices=STATE)

    def get_by_natural_key(self, element):
        return self.get(element=element)

    def __unicode__(self):
        return str(self.property)
