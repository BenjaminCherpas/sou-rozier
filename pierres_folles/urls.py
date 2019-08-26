# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from balafon.urls import urlpatterns as balafon_urlpatterns
from pierres_folles.course import urls as course_urls

from django.contrib import admin
admin.autodiscover()

#from coop_cms.feeds import ArticleFeed
#class ArticleFeed(ArticleFeed):
#    title = "Apidev"
#    link = "/rss/"

urlpatterns = [

    url(r'^', include('coop_cms.sitemap')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^course/', include(course_urls)),

    url(
        r'^photos/$',
        RedirectView.as_view(url=reverse_lazy(u'pl-gallery-list', args=[1]), permanent=False),
        name='pl-photologue-root'
    ),

    url(
        r'^photos/gallery/$',
        RedirectView.as_view(url=reverse_lazy(u'pl-gallery-list', args=[1]), permanent=False),
        name='pl-photologue-root'
    ),

    url(r'^photos/', include('photologue.urls')),
]

urlpatterns += balafon_urlpatterns