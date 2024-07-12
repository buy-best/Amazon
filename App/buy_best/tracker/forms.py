from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class ProductFilterForm(forms.Form):
    brand = forms.ChoiceField(required=False)
    min_price = forms.DecimalField(min_value=0, required=False)
    max_price = forms.DecimalField(min_value=0, required=False)
    rating = forms.ChoiceField(choices=[('', 'Any')] + [(i, i) for i in range(1, 6)], required=False)
    search = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices = [('', 'All Brands')] + [
            (brand, brand) for brand in Product.objects.values_list('brand', flat=True).distinct()
        ]

class ProductSortForm(forms.Form):
    sort_by = forms.ChoiceField(choices=[
        ('name', 'Name'),
        ('current_price', 'Price (Low to High)'),
        ('-current_price', 'Price (High to Low)'),
        ('rating', 'Rating'),
    ], required=False)