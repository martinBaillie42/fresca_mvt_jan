from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission

from mvt_admin.models import UserProfile
from mvt_admin.models import Domain
from mvt_admin.models import Experiment
from mvt_admin.models import Variant



## displaying the gmail user extnesion in the admin
## https://docs.djangoproject.com/en/1.5/
#
# Define an inline admin descriptor for UserExtension model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

## adds the models to admin
admin.site.register(Domain)
admin.site.register(Experiment)
admin.site.register(Variant)

# script to create users, groups, etc
if not User.objects.filter(username='martinmartin').count():
    # """You just created..."""
    # django superuser
    dsup = User(username="martinmartin", email="martin@martinbaillie.net", is_staff=True, is_superuser=True)
    dsup.set_password('martinmartin')
    dsup.save()
    # fresca superuser
    fsup = User(username="fsup", password="fsup", email="martin@martinbaillie.net", is_staff=True)
    fsup.set_password('fsup')
    fsup.save()
    # fresca normal user
    fnorm = User(username="fnorm", password="fnorm", email="martin@martinbaillie.net", is_staff=True)
    fnorm.set_password('fnorm')
    fnorm.save()
    # fresca super user group permission
        # User
        # Group
        # Domain
        # Experiment
        # Variant
    # fresca user group permission
        # Domain
        # Experiment
        # Variant

    # assign groups to users
if not Group.objects.filter(name='fresca_su').count():
    # fresca super user group permission
        # User
        # Group
        # Domain
        # Experiment
        # Variant
    fsug = Group(name='fresca_su')
    fsug.save()
    fsug.permissions.add(
        Permission.objects.get(codename='add_domain'),
        Permission.objects.get(codename='change_domain'),
        Permission.objects.get(codename='add_user'),
        Permission.objects.get(codename='change_user'),
        Permission.objects.get(codename='change_userprofile'),
        Permission.objects.get(codename='add_group'),
        Permission.objects.get(codename='change_group'), 
        Permission.objects.get(codename='add_experiment'),
        Permission.objects.get(codename='change_experiment'),
        Permission.objects.get(codename='add_variant'),
        Permission.objects.get(codename='change_variant'),       
    )
    fsug.user_set.add(fsup)
    fsug.save()
    # fresca user group permission
        # Domain
        # Experiment
        # Variant
    fnug = Group(name='fresca_normal')
    fnug.save()
    # will require 'view_domain'
    fnug.permissions.add(
        Permission.objects.get(codename='view_domain'),
        Permission.objects.get(codename='add_experiment'),
        Permission.objects.get(codename='change_experiment'),
        Permission.objects.get(codename='add_variant'),
        Permission.objects.get(codename='change_variant'),      
    )
    fnug.user_set.add(fnorm)
    fnug.save()

