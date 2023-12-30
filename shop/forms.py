from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", min_value=1, max_value=9)


class DiscountForm(forms.Form):
    code = forms.CharField(label="Coupon Code", max_length=5)
