from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from mvt_admin.models import UserExtension

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