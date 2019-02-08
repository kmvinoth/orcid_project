from django import forms
from .models import OrcidInvitation


class OrcidInvitationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrcidInvitationForm, self).__init__(*args, **kwargs)
        self.fields['researcher'].required = False
        self.fields['have_orcid'].required = False

        # tmp_choices = self.fields['have_orcid'].choices
        # del tmp_choices[0]
        # self.fields['have_orcid'].choices = tmp_choices
        #
        # tmp_choices = self.fields['researcher'].choices
        # del tmp_choices[0]
        # self.fields['researcher'].choices = tmp_choices

    class Meta:

        model = OrcidInvitation
        fields = ['researcher', 'have_orcid', 'message']
        labels = {'researcher': 'Are you a Researcher', "have_orcid": "Do you have ORCiD"}
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'cols': 35,
                                             'placeholder': 'Write your message here. Max 200 Characters.'}),
        }
