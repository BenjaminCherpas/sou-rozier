# -*- coding: utf-8 -*-
"""create newsletter item"""

from django.core.management.base import BaseCommand

from balafon.Crm.models import Action, ActionStatus, ActionType, Contact, Group
from pierres_folles.course.models import Category

class Command(BaseCommand):
    """force the creation of every newsletter items"""
    help = u"force the creation of every newsletter items"

    def handle(self, *args, **options):
        """command"""
        #look for emailing to be sent
        verbose = options.get('verbosity', 1)

        inscription_2015_6km = ActionType.objects.get(name=u'Inscription 2015 - 6 Km')
        inscription_2015_11km = ActionType.objects.get(name=u'Inscription 2015 - 11 Km')

        group_11 = Group.objects.get(name=u'11 Kilomètres')
        group_6 = Group.objects.get(name=u'6 Kilomètres')

        categories = list(Category.objects.all().order_by('year1'))
        categorie_problem_group = Group.objects.get_or_create(name='Probleme categorie')[0]

        for group, action_type in [(group_6, inscription_2015_6km), (group_11, inscription_2015_11km)]:
            for contact in group.contacts.all():
                found = False
                if contact.birth_date:
                    for cat in categories:
                        if contact.birth_date.year >= cat.year1 and contact.birth_date.year <= cat.year2:
                            contact.set_custom_field('categorie', cat.name)
                            found = True
                            categorie_problem_group.contacts.remove(contact)
                            categorie_problem_group.save()
                            break
                if not found:
                    print("> Probleme categorie", contact, contact.birth_date)
                    contact.set_custom_field('categorie', "Probleme")
                    categorie_problem_group.contacts.add(contact)
                    categorie_problem_group.save()
