from django import forms

from product.models import Product
from carts.models import Cart, CartItem


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'manufacturer',
            'category',
            'model',
            'price',
            'specifications',
            'stock',
            'discount'
        ]


class UpdateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'name',
            'manufacturer',
            'category',
            'model',
            'price',
            'specifications',
            'stock',
            'discount'
        ]

    def save(self, commit=True):
        product = self.instance
        product.name = self.cleaned_data['name']
        product.manufacturer = self.cleaned_data['manufacturer']
        product.category = self.cleaned_data['category']
        product.model = self.cleaned_data['model']
        product.price = self.cleaned_data['price']
        product.specifications = self.cleaned_data['specifications']
        product.stock = self.cleaned_data['stock']
        product.discount = self.cleaned_data['discount']

        if commit:
            product.save()

        return product


class AddToCartForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['quantity']

    def save(self, cart: Cart = None, product: Product = None):
        # cart = Cart.objects.get(id=cart_id)
        # product = Product.objects.get(id=product_id)

        quantity = self.cleaned_data['quantity']

        cart_item = None
        if product in cart.products.all():
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=quantity
            )
        return cart_item
