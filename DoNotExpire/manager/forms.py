from django import forms
from django.forms.widgets import CheckboxInput
from .models import Account, Character, Equipment


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'realm']

class CreateCharacterForm(forms.ModelForm):
    level = forms.IntegerField(min_value=1, max_value=99)

    class Meta:
        model = Character
        fields = ['name', 'char_class', 'level', 'expansion', 'hardcore', 'ladder']
        widgets = {
            "ladder": CheckboxInput()
        }
