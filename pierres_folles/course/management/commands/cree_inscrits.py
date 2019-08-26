# -*- coding: utf-8 -*-
"""create newsletter item"""

from django.core.management.base import BaseCommand

from balafon.Crm.models import Action, ActionStatus, ActionType, Contact, Group
from pierres_folles.course.models import Category, Course, Inscrit

class Command(BaseCommand):
    """force the creation of every newsletter items"""
    help = u"cree les inscrits a partir des contacts"

    def handle(self, *args, **options):
        """command"""
        #look for emailing to be sent
        verbose = options.get('verbosity', 1)

        #Course.objects.all().delete()

        inscription_2015_6km = ActionType.objects.get(name=u'Inscription 2015 - 6 Km')
        inscription_2015_11km = ActionType.objects.get(name=u'Inscription 2015 - 11 Km')

        group_11 = Group.objects.get(name=u'11 Kilomètres')
        group_6 = Group.objects.get(name=u'6 Kilomètres')

        for group, action_type in [(group_6, inscription_2015_6km), (group_11, inscription_2015_11km)]:

            course = Course.objects.get_or_create(name=group.name)[0]

            for contact in group.contacts.all():
                try:
                    inscription = contact.action_set.get(type=action_type)
                except:
                    print("Probleme inscription: ", contact)
                    continue

                Inscrit.objects.create(
                    course=course,
                    nom=contact.lastname,
                    prenom=contact.firstname,
                    gender=contact.gender,
                    birth_date=contact.birth_date,
                    city=contact.city.name if contact.city else '',
                    zip_code=contact.zip_code,
                    email=contact.email,
                    phone=contact.phone,
                    club=contact.get_custom_field('club')
                )

