# -*- coding: utf-8 -*-
"""context processor"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve, Resolver404

from coop_cms.models import get_article_class, Image, MediaFilter

from pierres_folles.course.models import Partner
from pierres_folles.course.forms import RunnerForm


def homepage(request):
    """"""
    article_class = get_article_class()
    context = {}

    context['primary_partners'] = Partner.objects.filter(is_archived=False, best_partner=True).order_by('ordering', '?')
    context['secondary_partners'] = Partner.objects.filter(is_archived=False, best_partner=False).order_by('ordering', '?')

    context['inscription_active'] = settings.INSCRIPTIONS_ACTIVE

    try:
        resolved = resolve(request.path)
    except Resolver404:
        resolved = None

    if resolved and resolved.url_name in ('coop_cms_view_article', 'coop_cms_edit_article'):

        is_homepage = article_class.objects.filter(
            slug=resolved.kwargs['slug'], homepage_for_site=Site.objects.get_current()
        ).exists()

        if is_homepage:
            context['runner_form'] = RunnerForm()

        context['is_homepage'] = is_homepage

    return context
