from django import forms

from manager.models import Account


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'name', 'realm'
        )
