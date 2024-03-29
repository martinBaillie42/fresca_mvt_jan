# extra packages:
# django-guardian
# django-http-proxy (dependent on httplib2)
# httplib2

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group, Permission

from mvt_admin.models import UserProfile
from mvt_admin.models import Domain
from mvt_admin.models import Experiment
from mvt_admin.models import Variant
from mvt_admin.models import Element
from mvt_admin.models import Declaration

# to set up the MyAdminSite/admin_site object
from django.contrib.admin import AdminSite
from django.views.decorators.cache import never_cache

# used by the MyAdminSite index method
# from functools import update_wrapper
from django.http import Http404, HttpResponseRedirect
# from django.contrib.admin import ModelAdmin, actions
from django.contrib.admin.forms import AdminAuthenticationForm
# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.contrib.contenttypes import views as contenttype_views
# from django.views.decorators.csrf import csrf_protect
# from django.db.models.base import ModelBase
# from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
# from django.views.decorators.cache import never_cache
# from django.conf import settings

from django.conf.urls import patterns


class MyAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_dict = {}
        user = request.user
        # prevents access to the admin index page
        if not user.is_superuser:
            return HttpResponseRedirect(reverse('admin:mvt_admin_domain_changelist'))

        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)

            if has_module_perms:
                perms = model_admin.get_model_perms(request)

                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.module_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': app_label.title(),
                            'app_url': reverse('admin:app_list', kwargs={'app_label': app_label},
                                               current_app=self.name),
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }

        # Sort the apps alphabetically.
        app_list = list(six.itervalues(app_dict))
        app_list.sort(key=lambda x: x['name'])

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        context = {
            'title': _('Site administration'),
            'app_list': app_list,
        }
        context.update(extra_context or {})
        return TemplateResponse(request, self.index_template or
                                         'admin/index.html', context,
                                current_app=self.name)

    def app_index(self, request, app_label, extra_context=None):
        user = request.user
        # prevents access of the mvt_admin app module list
        if not user.is_superuser and app_label == 'mvt_admin':
            # return HttpResponseRedirect(app_label)
            return HttpResponseRedirect(reverse('admin:mvt_admin_domain_changelist'))

        has_module_perms = user.has_module_perms(app_label)
        app_dict = {}
        for model, model_admin in self._registry.items():
            if app_label == model._meta.app_label:
                if has_module_perms:
                    perms = model_admin.get_model_perms(request)

                    # Check whether user has any perm for this module.
                    # If so, add the module to the model_list.
                    if True in perms.values():
                        info = (app_label, model._meta.module_name)
                        model_dict = {
                            'name': capfirst(model._meta.verbose_name_plural),
                            'perms': perms,
                        }
                        if perms.get('change', False):
                            try:
                                model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info,
                                                                  current_app=self.name)
                            except NoReverseMatch:
                                pass
                        if perms.get('add', False):
                            try:
                                model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                            except NoReverseMatch:
                                pass
                        if app_dict:
                            app_dict['models'].append(model_dict),
                        else:
                            # First time around, now that we know there's
                            # something to display, add in the necessary meta
                            # information.
                            app_dict = {
                                'name': app_label.title(),
                                'app_url': '',
                                'has_module_perms': has_module_perms,
                                'models': [model_dict],
                            }
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: x['name'])
        context = {
            'title': _('%s administration') % capfirst(app_label),
            'app_list': [app_dict],
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context, current_app=self.name)


admin_site = MyAdminSite()

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
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# register UserAdmin with admin_site
admin_site.register(User, UserAdmin)


class ExperimentInline(admin.TabularInline):
    model = Experiment
    fields = ('selflink', 'name', 'experiment_type', 'status', 'date_start', 'date_end',)
    # readonly_fields = ('selflink','experiment_type','name')
    readonly_fields = ('selflink',)
    extra = 0


class DomainAdmin(admin.ModelAdmin):
    inlines = [ExperimentInline]
    # this prevents a non-superuser from seeing the users who can access this domain
    # need to make fresca_su so it can see it.
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('user')
        return super(DomainAdmin, self).get_form(request, obj, **kwargs)


class VariantInline(admin.TabularInline):
    model = Variant
    fields = ('selflink', 'number',)
    readonly_fields = ('selflink',)
    extra = 0


class ExperimentAdmin(admin.ModelAdmin):
    inlines = [VariantInline]


class DeclarationInline(admin.TabularInline):
    model = Declaration
    extra = 0


class ElementInline(admin.TabularInline):
    inlines = [DeclarationInline]
    model = Element
    extra = 0
#  https://github.com/Soaa-/django-nested-inlines

class VariantAdmin(admin.ModelAdmin):
    inlines = [ElementInline]
    model = Variant
    fields = ('number',)

    class Media:
        css = {
            'all': ('jquery-ui-1.10.3.custom.css', 'variant.css',)
        }


class ElementAdmin(admin.ModelAdmin):
    inlines = [DeclarationInline]
    model = Element


## adds the models to admin
admin_site.register(Domain, DomainAdmin)
admin_site.register(Experiment, ExperimentAdmin)
admin_site.register(Variant, VariantAdmin)
admin_site.register(Element, ElementAdmin)
admin_site.register(Declaration)
admin_site.register(Group)

# Wed TODO
# edit variant page so it links to the business end of the editing.
# variant page will require it's own template, which will need to be a way of incorporating 
# the original CK MVT demo I did back in the autumn. Might need to have the variants on the 
# experiment page link to a non-Admin page.
# original rudefish demo is here D:\xampp\htdocs\rudefish_prototype

# TODO
# httpproxy has a new version,that could be worth investigating
# current version cannot be overwritten, but could be amended

# TODO: remove revproxy - uses deprecated django methods


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

if not Domain.objects.filter(name='www.cathkidston.com').count():
    d_rec = Domain(name='www.cathkidston.com', )
    d_rec.save()

if not Experiment.objects.filter(name="experiment1").count():
    d_row = Domain.objects.get(name='www.cathkidston.com')
    e_rec = Experiment(
        domain_id=d_row.id,
        date_start='2014-01-01' ,
        date_end= '2015-01-01',
        experiment_type='MVT', name="experiment1",
        status='UNPUBLISHED', uri='Home.ice', page_type='home', page_identifier='basic_layout',
        experiment_js='.'
    )
    e_rec.save()

    e_row = Experiment.objects.get(name='experiment1')
    v_rec = Variant(
        experiment_id=e_row.id,
        number=1,
        state='active',
    )
    v_rec.save()

    # Element
    v_row = Variant.objects.get(number=1)
    el_rec = Element(
        variant_id=v_row.id,
        selector='h1',
        state='active',
    )
    el_rec.save()

    #  Declaration
    el_row = Element.objects.get(selector='h1')
    de_rec = Declaration(
        element_id=el_row.id,
        property='width',
        value='100px',
        state='active',
    )
    de_rec.save()

    de2_rec = Declaration(
        element_id=el_row.id,
        property='height',
        value='200px',
        state='active',
    )
    de2_rec.save()