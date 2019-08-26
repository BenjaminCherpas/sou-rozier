#-*- coding: utf-8 -*-

import floppyforms as forms

from balafon.Crm.models import Group
from balafon.Profile.forms import MinimalUserRegistrationForm


class ParentRegistrationForm(MinimalUserRegistrationForm):

    parents_code = forms.CharField(
        required=True,
        label='Code Parent',
        widget=forms.TextInput(attrs={'placeholder': u'Entrez le code qui a été donné à votre enfant'})
    )

    def __init__(self, *args, **kwargs):
        super(ParentRegistrationForm, self).__init__(*args, **kwargs)
        parents_group = Group.objects.get_or_create(name='Parents')[0]
        self.fields['groups_ids'].initial = unicode(parents_group.id)

    def clean_parents_code(self):
        if self.cleaned_data['parents_code'] != 'parents-42810':
            raise forms.ValidationError("Le code n'est pas correct. Vérifiez le code ou contactez nous")
        return self.cleaned_data['parents_code']