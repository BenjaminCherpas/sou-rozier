# -*- coding: utf-8 -*-
"""create newsletter item"""

from django.core.management.base import BaseCommand

from balafon.Crm.models import Action, ActionStatus, ActionType, Contact, Group

class Command(BaseCommand):
    """force the creation of every newsletter items"""
    help = u"force the creation of every newsletter items"

    def handle(self, *args, **options):
        """command"""
        #look for emailing to be sent
        verbose = options.get('verbosity', 1)

        recu = ActionStatus.objects.get_or_create(name=u'Reçu')[0]
        paye = ActionStatus.objects.get_or_create(name=u'Payé')[0]
        probleme = ActionStatus.objects.get_or_create(name=u'Problème')[0]
        valide = ActionStatus.objects.get_or_create(name=u'Validé')[0]
        paiement_mais_probleme = ActionStatus.objects.get_or_create(name=u'Paiement Ok - Probleme inscription')[0]

        inscription_2015 = ActionType.objects.get(name=u'Inscription 2015')

        inscription_2015_6km = ActionType.objects.get_or_create(name=u'Inscription 2015 - 6 Km')[0]
        inscription_2015_11km = ActionType.objects.get_or_create(name=u'Inscription 2015 - 11 Km')[0]

        paiement_ok = Group.objects.get(name=u'Paiement Ok')
        inscription_ok = Group.objects.get(name=u'Inscription Ok')
        inscription_probleme = Group.objects.get(name=u'Inscription Problème')

        for action_type in (inscription_2015_11km, inscription_2015_6km):
            for status in (recu, paye, probleme, valide, paiement_mais_probleme):
                action_type.allowed_status.add(status)
            action_type.save()

        group_11 = Group.objects.get(name=u'11 Kilomètres')
        group_6 = Group.objects.get(name=u'6 Kilomètres')
        goup_probleme_categorie = Group.objects.get(name=u'Probleme categorie')

        participation_2015 = Group.objects.get(name=u'Participation 2015')

        non_club_ids = [
            group_11, group_6, participation_2015, paiement_ok, inscription_ok, inscription_probleme,
            goup_probleme_categorie
        ]

        for group, action_type in [(group_6, inscription_2015_6km), (group_11, inscription_2015_11km)]:
            for contact in group.contacts.all():

                #contact.action_set.filter(type=action_type).delete()

                if contact.action_set.filter(type=action_type).exists():
                    #dispose deja d'une inscription --> Ok
                    continue

                try:
                    inscription = contact.action_set.get(type=inscription_2015)
                except:
                    print("Probleme inscription: ", contact)
                    continue

                clubs = contact.group_set.exclude(id__in=[gr.id for gr in non_club_ids])
                if clubs.count() >= 1:
                    contact.set_custom_field("Club", clubs[0].name)
                elif clubs.count() == 0:
                    contact.set_custom_field("Club", "Sans club")

                action = Action.objects.create(
                    type=action_type,
                    planned_date=inscription.planned_date,
                    amount=inscription.amount,
                    subject=inscription.subject
                )

                if contact in inscription_probleme.contacts.all():
                    if contact in paiement_ok.contacts.all():
                        action.status = paiement_mais_probleme
                    else:
                        action.status = probleme
                elif contact in inscription_ok.contacts.all():
                    action.status = valide
                elif contact in paiement_ok.contacts.all():
                    action.status = paye
                else:
                    action.status = recu

                action.contacts.add(contact)

                action.save()

# #from course.models import Course, Inscrit
# c11 = Course.objects.get(name__icontains='11')
# for i, ins in enumerate(c11.inscrit_set.order_by('nom', 'prenom')):
#    ins.numero = i + 1
#    ins.save()
