from django import forms
from django.forms.widgets import CheckboxInput

from manager.models import Character


class CreateCharacterForm(forms.ModelForm):
    level = forms.IntegerField(min_value=1, max_value=99)

    class Meta:
        model = Character
        fields = ['name', 'char_class', 'level', 'expansion', 'hardcore', 'ladder']
        widgets = {
            "ladder": CheckboxInput(attrs={'checked': False}),
            "expansion": CheckboxInput(attrs={'checked': True}),
            "hardcore": CheckboxInput(attrs={'checked': False})
        }
