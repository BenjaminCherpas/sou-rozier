# -*- coding: utf-8 -*-

from datetime import datetime, date, time, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from balafon.Crm.models import Contact


class Partner(models.Model):
    """Sponsors"""
    name = models.CharField(max_length=100, verbose_name=_(u'Nom'))
    url = models.URLField(default='', blank=True, verbose_name=_(u'URL'))
    logo = models.ImageField(blank=True, upload_to='partners', default='', verbose_name=_(u'logo'))
    is_archived = models.BooleanField(default=True, verbose_name=_(u'archivé'))
    best_partner = models.BooleanField(default=False, verbose_name=_(u'partenaire majeur'))
    ordering = models.IntegerField(default=0, verbose_name=_(u"order d'affichage"))

    class Meta:
        verbose_name = _(u'Sponsor')
        verbose_name_plural = _(u'Sponsors')
        ordering = ('name',)

    def __str__(self):
        return self.name


class License(models.Model):
    name = models.CharField(max_length=200, verbose_name=_(u"Nom"))
    nb_required = models.BooleanField(default=True, verbose_name=_(u"No de license requis"))
    short_name = models.CharField(max_length=100, verbose_name=_(u"Nom court"), default='', blank=True)

    class Meta:
        verbose_name = _(u'Licence')
        verbose_name_plural = _(u'Licence')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Competition(models.Model):
    name = models.CharField(max_length=100, verbose_name=_(u"Nom"))
    price = models.DecimalField(verbose_name=_(u'Prix Jour J'), max_digits=5, decimal_places=2)
    price_before = models.DecimalField(verbose_name=_(u'Prix pré-inscription'), max_digits=5, decimal_places=2)
    before_date = models.DateField(verbose_name=_(u'Date limite pré-inscription'))
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = _(u'Competition')
        verbose_name_plural = _(u'Competitions')
        ordering = ('id',)

    def __str__(self):
        return self.name


class InfoSource(models.Model):
    """Comment un coureur a connu la course"""
    name = models.CharField(max_length=100, verbose_name=_(u"Nom"))
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name = _(u"Source d'information")
        verbose_name_plural = _(u"Source d'informations")
        ordering = ('ordering', 'id')

    def __str__(self):
        return self.name


class Runner(Contact):
    """"""
    competition = models.ForeignKey(Competition, verbose_name=_(u"Course"))
    club = models.CharField(max_length=100, verbose_name=_(u"Club"), blank=True, default="")
    license = models.ForeignKey(
        License, default=None, blank=True, null=True, verbose_name=_(u"Licence"),
        help_text=_(
            u"Si vous n'êtes pas licencié, sélectionnez 'Cerificat médical'"
        )
    )
    license_number = models.CharField(max_length=100, default='', blank=True, verbose_name=_(u"N° de licence"))
    scan = models.FileField(
        upload_to="licenses", verbose_name=_(u"Fichier"),
        help_text=_(
            u"Joindre un scan de la license sportive ou du certificat médical. "
            u"Merci de ne pas dépasser 2Mo comme taille de fichier."
        )
    )
    payment_url = models.TextField(default='', blank=True)
    source_info = models.ForeignKey(InfoSource, default=None, null=True, on_delete=models.SET_NULL)

    def get_price(self):
        if self.runner.created.date() < self.competition.before_date:
            return self.competition.price_before
        else:
            return self.competition.price

    def get_payplug_amount(self):
        return int(self.get_price() * 100)

    class Meta:
        verbose_name = _(u'Participant')
        verbose_name_plural = _(u'Participants')
        ordering = ('lastname', 'firstname')


class InstantPaymentNotification(TimeStampedModel):
    """track every PayPlug IPN"""
    runner = models.ForeignKey(Runner)
    body = models.TextField(default='', blank=True)
    signature = models.TextField(default='', blank=True)
    is_ssl_valid = models.BooleanField(default=False, verbose_name=_(u'SSL message is ok'))
    is_amount_valid = models.BooleanField(default=False, verbose_name=_(u'received amount is ok'))
    is_email_valid = models.BooleanField(default=False, verbose_name=_(u'received email is ok'))
    is_contact_valid = models.BooleanField(default=False, verbose_name=_(u'received customer id is ok'))
    transaction_id = models.IntegerField(default=0)
    signature_ok = models.BooleanField(default=False)

    def __str__(self):
        return u'{0}'.format(self.runner)


class Category(models.Model):

    name = models.CharField(max_length=100)
    year1 = models.IntegerField()
    year2 = models.IntegerField()

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')
        ordering = ('year1',)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    heure_depart = models.TimeField(default=time(16, 0))

    def __str__(self):
        return self.name


class Inscrit(models.Model):
    GENDER_CHOICE = (
        (Contact.GENDER_MALE, u'Homme'),
        (Contact.GENDER_FEMALE, u'Femme'),
    )

    numero = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICE)
    birth_date = models.DateField()
    category = models.ForeignKey(Category, blank=True, default=None, null=True)
    arrivee = models.TimeField(blank=True, null=True, default=None)
    contact = models.ForeignKey(Contact, default=None, blank=True, null=True)
    city = models.CharField(default='', max_length=100, blank=True)
    zip_code = models.CharField(default='', max_length=100, blank=True)
    email = models.EmailField(default='', blank=True)
    club = models.CharField(default='', max_length=100, blank=True)
    phone = models.CharField(default='', max_length=100, blank=True)

    class Meta:
        verbose_name = _(u'Inscrit')
        verbose_name_plural = _(u'Inscrits')
        ordering = ('numero', 'nom', 'prenom', 'arrivee')

    def __str__(self):
        return u'{0} - {1}'.format(self.numero, self.nom)

    def fullname(self):
        return u'{0} {1}'.format(self.nom, self.prenom)

    def temps(self):
        if self.arrivee:
            heure_arrivee = self.arrivee
        else:
            heure_arrivee = datetime.now().time()
        dt2 = datetime.combine(date.today(), heure_arrivee)
        dt1 = datetime.combine(date.today(), self.course.heure_depart)
        return dt2 - dt1

    def calcul_categorie(self):
        if self.category:
            return self.category
        categories = list(Category.objects.all().order_by('year1'))
        for cat in categories:
            if self.birth_date.year >= cat.year1 and self.birth_date.year <= cat.year2:
                return cat
        return None

    def save(self, *args, **kwargs):
        self.category = self.calcul_categorie()
        return super(Inscrit, self).save(*args, **kwargs)
