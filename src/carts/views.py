from django.shortcuts import render, get_object_or_404, redirect
from operator import attrgetter
from decimal import Decimal
from django.views.generic import ListView
from .forms import AddProductToCartForm
from .models import Cart, CartItem
from product.models import Product
from product.views import get_product_queryset


class CartListView(ListView):
    template_name = 'carts/carts_list.html'
    queryset = Cart.objects.all()


def get_cart_detail_view(request, id, p_id=None):
    template_name = 'carts/cart_detail.html'
    context = {}

    obj = get_object_or_404(Cart, id=id)
    if p_id:
        product = get_object_or_404(Product, id=p_id)
        obj.products.remove(product)

    # form = AddProductToCartForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save(cart, product)
    #     form = AddProductToCartForm()

    # context['form'] = form

    items = []
    for product in obj.products.all():
        cart_item = CartItem.objects.get(product=product, cart=obj)
        item = {
            'cart_item': cart_item,
            'total': get_final_price(
                product.price, cart_item.quantity, product.discount
            )
        }
        items.append(item)

    context['object'] = obj
    context['items'] = items

    total_amount = str(sum([Decimal(item['total']) for item in items]))

    if "." in total_amount:
        total_amount = total_amount[:total_amount.index(".") + 3]

    context['total_amount'] = total_amount
    return render(request, template_name, context)


def get_final_price(original_price, quantity, discount=0.0):
    price = original_price
    if discount > 0.0:
        discount_amount = Decimal(original_price) * Decimal(discount) / 100
        price -= discount_amount
    result = str(price*quantity)
    return result[:result.index(".")+3] if "." in result else result


def add_product_to_cart_view(request, id, query=None):
    template_name = 'carts/cart_add_product_list.html'
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    cart = get_object_or_404(Cart, id=id)

    products = sorted(
        get_product_queryset(query), key=attrgetter('name'), reverse=True
    )
    print(products)
    context['products'] = products
    context['cart'] = cart

    return render(request, template_name, context)


def cart_add_product_detail_view(request, cart_id, product_id):
    cart = get_object_or_404(Cart, id=id)
    product = get_object_or_404(Product, id=product_id)
    context = {}

    form = AddProductToCartForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(cart, product)
        form = AddProductToCartForm()

    context['form'] = form

    return render(request, 'carts/cart_add_product_detail.html', context)


def remove_product_view(request, cart_id):
    obj = get_object_or_404(Product, id=id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object": obj
    }
    return render(request, "products/product_delete.html", context)
