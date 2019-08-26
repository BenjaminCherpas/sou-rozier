# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib.admindocs import urls as admindocs_urls

from balafon.urls import urlpatterns as balafon_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('coop_cms.sitemap')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include(admindocs_urls)),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
]

urlpatterns += balafon_urlpatterns
