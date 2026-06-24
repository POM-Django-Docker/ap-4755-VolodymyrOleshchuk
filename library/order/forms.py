from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("book", "plated_end_at")


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("user", "book", "plated_end_at", "end_at")