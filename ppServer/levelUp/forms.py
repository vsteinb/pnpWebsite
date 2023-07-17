
from django import forms

from character.models import Charakter
from httpChat.forms import M2MSelect

from character.models import Affektivität


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Charakter
        widgets = {"persönlichkeit": M2MSelect()}
        fields = [
            "name",
            "persönlichkeit",

            "gewicht",
            "größe",
            "alter",
            "geschlecht",
            "sexualität",
            "beruf",
            "präf_arm",
            "religion",
            "hautfarbe",
            "haarfarbe",
            "augenfarbe",

            "persönlicheZiele",
            "notizen"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ["name", "persönlichkeit", "gewicht", "größe", "alter", "beruf", "religion"]
        for field in required_fields:
            self.fields[field].label += "*"
            self.fields[field].required = True

        if kwargs["instance"].larp:
            self.fields['beruf'].widget = forms.HiddenInput()


class AffektivitätForm(forms.ModelForm):
    class Meta:
        model = Affektivität
        fields = ["name", "wert", "notizen"]
