from django import forms

from .models import FTTx
from .models import ADSS
from .models import Tip8
from .models import Vkanal
from .models import Vgrunt
from .models import Universalnyj
from .models import Ognestojkij
from .models import Raspredelitelnyj


class FTTxForm(forms.ModelForm):
    class Meta:
        model = FTTx
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class ADSSForm(forms.ModelForm):
    class Meta:
        model = ADSS
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class Tip8Form(forms.ModelForm):
    class Meta:
        model = Tip8
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class VkanalForm(forms.ModelForm):
    class Meta:
        model = Vkanal
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class VgruntForm(forms.ModelForm):
    class Meta:
        model = Vgrunt
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class RaspredForm(forms.ModelForm):
    class Meta:
        model = Raspredelitelnyj
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class OgnestoiForm(forms.ModelForm):
    class Meta:
        model = Ognestojkij
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }


class UniversForm(forms.ModelForm):
    class Meta:
        model = Universalnyj
        fields = (
            'name',
            'volokno',
            'kN',
            'price',
            'link',
        )
        widgets = {
            'name': forms.TextInput,
            'kN': forms.TextInput
        }