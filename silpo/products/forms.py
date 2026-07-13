from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    name = forms.CharField(
        label='Product Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "w-full rounded-lg border border-gray-600 bg-gray-700 px-4 py-3 text-white placeholder-gray-400 focus:border-indigo-500 focus:outline-none",
            "placeholder": "Product name",
        })
    )
    
    price = forms.DecimalField(
        label='Price',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "step": "0.01",
            "class": "w-full rounded-lg border border-gray-600 bg-gray-700 px-4 py-3 text-white placeholder-gray-400 focus:border-indigo-500 focus:outline-none",
            "placeholder": "0.00",
        })
    )

    category = forms.ModelChoiceField(
        queryset=None,
        label='Category',
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border border-gray-600 bg-gray-700 px-4 py-3 text-white focus:border-indigo-500 focus:outline-none",
        })
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "slug",
            "description",
            "price",
        ]

        widgets = {
            "slug": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-600 bg-gray-700 px-4 py-3 text-white placeholder-gray-400 focus:border-indigo-500 focus:outline-none",
                "placeholder": "product-slug",
            }),
            "description": forms.Textarea(attrs={
                "rows": 5,
                "class": "w-full rounded-lg border border-gray-600 bg-gray-700 px-4 py-3 text-white placeholder-gray-400 focus:border-indigo-500 focus:outline-none",
                "placeholder": "Product description",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from categories.models import Category
        self.fields['category'].queryset = Category.objects.all()