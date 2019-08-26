# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import floppyforms as forms
from balafon.Crm.models import Contact
from balafon.Crm.forms import ModelFormWithCity


from pierres_folles.course.models import Runner, Competition


class RunnerForm(ModelFormWithCity):
    """formulaire d'inscription"""

    GENDER_CHOICES = (
        ('', _(u'')),
        (Contact.GENDER_MALE, _(u'Mr')),
        (Contact.GENDER_FEMALE, _(u'Mrs')),
    )

    accept_rules = forms.BooleanField(
        label=u"Je reconnais avoir pris connaissance du réglement et en accepte les modalités",
        help_text='Cocher la case pour accepter',
        required=True,
    )

    class Meta:
        model = Runner
        fields = (
            'gender', 'lastname', 'firstname', 'birth_date', 'email', 'address', 'zip_code', 'city', 'country', 'phone',
            'competition', 'club', 'license', 'license_number', 'scan', 'source_info', 'notes', 'accept_rules'
        )

    def __init__(self, *args, **kwargs):
        super(RunnerForm, self).__init__(*args, **kwargs)
        self.fields['country'].widget = forms.HiddenInput()
        self.fields['gender'].choices = RunnerForm.GENDER_CHOICES

        competition_queryset = Competition.objects.filter(is_archived=False)

        self.fields['competition'].queryset = competition_queryset

        required_fields = (
            'gender', 'lastname', 'firstname', 'birth_date', 'email', 'address', 'zip_code', 'city', 'phone', 'license',
        )
        for field in required_fields:
            self.fields[field].required = True

        self.fields['birth_date'].help_text = mark_safe(u'JJ/MM/AAAA &nbsp; &nbsp; &nbsp; exemple 14/02/1982')
        self.fields['license_number'].help_text = u'Seulement pour les licenciés'
        self.fields['club'].help_text = u'Seulement pour les licenciés'

        self.fields['notes'].label = u"Une question ou un message à nous laisser?"
        self.fields['notes'].help_text = u"Vous pouvez aussi nous dire quelles sont vos attentes pour cette course."

        self.fields['competition'].help_text = mark_safe(
            u'. &nbsp; - &nbsp; '.join(
                [
                    u'{0}: {1:02}€ avant le {2:%d/%m}, {3:02}€ après'.format(
                        competition.name,
                        competition.price_before,
                        competition.before_date,
                        competition.price
                    )
                    for competition in competition_queryset
                ]
            )
        )

    def clean_notes(self):
        notes = self.cleaned_data['notes']
        if len(notes) > 20000:
            raise forms.ValidationError("Votre commmentaire ne peut excéder 20000 caractères")
        return notes
