from carts.models import Cart, CartItem


def cart_processor(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(account=request.user)
        no_products = 0
        for product in cart.products.all():
            products_in_cart = CartItem.objects.get(
                cart=cart,
                product=product
            ).quantity
            no_products += products_in_cart
        str_no_products = f'({no_products})'
    return {
        'cart_items': str_no_products,
        'cart_url': cart.get_absolute_url()
    }
