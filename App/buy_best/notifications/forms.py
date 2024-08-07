from django import forms
from .models import PriceAlert

class PriceAlertForm(forms.ModelForm):
    class Meta:
        model = PriceAlert
        fields = ['target_price']
        widgets = {
            'target_price': forms.NumberInput(attrs={'step': '0.01'})
        }