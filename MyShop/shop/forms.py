from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'delivery_method', 'delivery_address', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваше ПІБ'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваш телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ваш email'}),
            'delivery_method': forms.Select(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть вашу адресу доставки'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Додати коментар', 'rows': 3}),
        }
