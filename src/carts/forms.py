from django import forms
from .models import Cart, CartItem
from product.models import Product


class RawProductForm(forms.Form):
    title       = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    description = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description",
                                    "class": "new-class-name two",
                                    "id": "my-id-for-textarea",
                                    "rows": 20,
                                    'cols': 120
                                }
                            )
                        )
    price       = forms.DecimalField(initial=199.99)


class RawAddProductToCartForm(forms.Form):
    product_name       = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    product_category = forms.CharField(
                        required=False, 
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description",
                                    "class": "new-class-name two",
                                    "id": "my-id-for-textarea",
                                    "rows": 20,
                                    'cols': 120
                                }
                            )
                        )
    quantity       = forms.DecimalField(initial=199.99)



class AddProductToCartForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['quantity']

    def save(self, cart, product):
        # cart = Cart.objects.get(id=cart_id)
        # product = Product.objects.get(id=product_id)

        quantity = self.cleaned_data['quantity']

        cart_item = CartItem()
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += quantity
            cart_item.save()
        except:
            cart_item = CartItem.objects.create(product, cart, quantity)
        return cart_item