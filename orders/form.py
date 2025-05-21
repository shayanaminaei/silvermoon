from django import forms
from .models import Order, Address
from productions.models import Color, Product


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='تعداد')
    color = forms.ModelChoiceField(queryset=Color.objects.all(), label='رنگ')  # استفاده از ModelChoiceField

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product:
            self.fields['color'].queryset = product.colors.all()  # فقط رنگ‌های مربوط به محصول خاص


class OrderForm(forms.Form):
    address = forms.ModelChoiceField(queryset=Address.objects.none(), label='آدرس')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user_id=user.id)
