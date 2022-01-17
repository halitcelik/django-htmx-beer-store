from django import forms
from .models import Beer


class BeerForm(forms.ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Beer
        fields = (
            "name",
            "category",
            "style",
        )


class BeerDescriptionForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = ("descript",)


class BeerDetailsForm(forms.ModelForm):
    class Meta:
        model = Beer
        fields = (
            "abv",
            "ibu",
            "srm",
            "upc",
        )
