from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
# from django.shortcuts import redirect
# from django.http import Http404, HttpResponseRedirect



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from mvt_admin.admin import admin_site
import mvt_admin
from mvt_admin import views
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fresca_mvt_jan.views.home', name='home'),
    # url(r'^fresca_mvt_jan/', include('fresca_mvt_jan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^fresca_mvt_jan/admin/', include(admin_site.urls)),
    # url(r'^(?P<url>.*)$', 'httpproxy.views.proxy'),
    # url(r'^fresca_mvt_jan/admin/', "revproxy.proxy.proxy_request", {"destination": "http://www.cathkidston.com"}),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^fresca_mvt_jan/admin/', include(admin_site.urls)),
    # url(r'^fresca_mvt_jan/redirect/exturi=(?P<exturi>\w{1,50})', mvt_admin.views.index, name="index"),
    url(r'^fresca_mvt_jan/redirect/$', mvt_admin.views.index, name="index"),
)

urlpatterns += staticfiles_urlpatterns()
