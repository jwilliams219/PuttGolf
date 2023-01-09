
from django import forms
from django.forms import ModelForm
from .models import Drink


class addDrink(ModelForm):
    class Meta:
        model = Drink
        fields = "__all__"


class deleteDrink(forms.Form):
    drinkList = Drink.objects.all()
    drink = forms.ModelChoiceField(queryset=drinkList, required=False)


class editDrink(ModelForm):
    drinkList = Drink.objects.all()
    drink = forms.ModelChoiceField(queryset=drinkList, required=False)

    class Meta:
        model = Drink
        fields = ['drink', 'name', 'price', 'instructions']
