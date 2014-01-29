from django.conf.urls import patterns, include, url
# from django.http import Http404, HttpResponseRedirect
# from django.shortcuts import redirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from mvt_admin.admin import admin_site
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fresca_mvt_jan.views.home', name='home'),
    # url(r'^fresca_mvt_jan/', include('fresca_mvt_jan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^fresca_mvt_jan/admin/', include(admin_site.urls)),
    # url(r'^exturl/(?P<exturi>)$', redirect_to({'url': 'http://www.cathkidston.com'})),
    url(r'^fresca_mvt_jan/admin/', include(admin_site.urls)),
)
