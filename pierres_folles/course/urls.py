# -*- coding: utf-8 -*-

from django.conf.urls import url

from pierres_folles.course.views import RunnerView, InstantPaymentNotificationView, InscriptionsXlsView, ClassementView


urlpatterns = [
    url(
        r'^inscription/$',
        RunnerView.as_view(),
        name="course_inscription"
    ),

    url(
        r'^ipn/(?P<contact_uuid>[\w\d-]+)$',
        InstantPaymentNotificationView.as_view(),
        name='course_instant_payment_notification'
    ),

    url(
        r'^export-inscriptions/$',
        InscriptionsXlsView.as_view(),
        name='course_export_inscriptions'
    ),

    url(
        r'classement/$',
        ClassementView.as_view(),
        name='course_classement'
    ),
]
