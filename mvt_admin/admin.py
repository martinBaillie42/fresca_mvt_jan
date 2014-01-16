from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from mvt_admin.models import UserExtension
from mvt_admin.models import Domain
from mvt_admin.models import Experiment
from mvt_admin.models import Variant




## displaying the gmail user extnesion in the admin
## https://docs.djangoproject.com/en/1.5/

# Define an inline admin descriptor for UserExtension model
# which acts a bit like a singleton
class UserExtensionInline(admin.StackedInline):
    model = UserExtension
    can_delete = False
    verbose_name_plural = 'userextension'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserExtensionInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)





## enable user to see only the domains that are assigned to them
class DomainAdmin(admin.ModelAdmin):

    # readonly_fields = ('name','user',)
    

    # https://docs.djangoproject.com/en/1.5/ref/contrib/admin/#django.contrib.admin.ModelAdmin.queryset
    def queryset(self, request):
        qs = super(DomainAdmin, self).queryset(request)

        # If super-user, show all domains
        if request.user.is_superuser:
            return qs

        return qs.filter(user=request.user)

    # for non superusers make domain uneditable
    # http://stackoverflow.com/questions/11601148/making-a-field-readonly-in-django-admin
    #
    # this https://docs.djangoproject.com/en/1.6/topics/auth/customizing/#custom-permissions
    # might be a better way of doing it
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ('name','user',)
        return self.readonly_fields

# update the modified DomainAdmin class
admin.site.register(Domain, DomainAdmin)




## adds the models to admin
admin.site.register(Experiment)
admin.site.register(Variant)