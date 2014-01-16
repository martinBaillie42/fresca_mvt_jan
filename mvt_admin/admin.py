from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


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