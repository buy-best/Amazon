# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('seller', 'Seller')
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')  # Include fields you want to edit
    
class BalanceForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class UserPreferenceForm(forms.Form):
    price_min = forms.IntegerField(label='Minimum Price', required=False)
    price_max = forms.IntegerField(label='Maximum Price', required=False)
    product_type = forms.CharField(label='Product Type', max_length=100, required=False)
    brand = forms.CharField(label='Brand', max_length=100, required=False)
    keywords = forms.CharField(label='Keywords', max_length=200, required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super(UserPreferenceForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['price_min'].initial = instance.price_min
            self.fields['price_max'].initial = instance.price_max
            self.fields['product_type'].initial = instance.product_type
            self.fields['brand'].initial = instance.brand
            self.fields['keywords'].initial = instance.keywords