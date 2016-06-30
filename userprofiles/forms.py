from django import forms
from mainsite import models


class DomainForm(forms.ModelForm):
    class Meta:
        model = models.Domain
        fields = ('domain',)
