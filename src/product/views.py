from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseNotFound
from operator import attrgetter
from product.models import Product
from product.constants import CATEGORIES
from product.forms import (
    CreateProductForm,
    UpdateProductForm,
    AddToCartForm,
)
from account.models import Account
from carts.models import CartItem, Cart


def get_all_products_view(request, slug=None):
    template_name = 'product/list_products.html'
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    query = ""
    tuery = ""
    count = 0
    if request.GET:
        query = request.GET.get('q', '')
        tuery = request.GET.get('t', '')
        context['query'] = str(query)
        context['tuery'] = str(tuery)
        count = int(request.GET.get('s', ''))

    count += 1
    context['count'] = str(count)

    products = sorted(
        get_product_queryset(query), key=attrgetter('name'), reverse=True
    )

    context['products'] = products

    # if slug:
    #     product = get_object_or_404(Product, slug=slug)
    #     product.delete()

    # products = Product.objects.all()
    # context = {
    #     'products': products,
    # }
    return render(request, template_name, context)


# def add_product_to_cart_view(request, id, query=None):
#     template_name = 'carts/cart_add_product_list.html'
#     context = {}

#     query = ""
#     if request.GET:
#         query = request.GET.get('q', '')
#         context['query'] = str(query)

#     cart = get_object_or_404(Cart, id=id)

#     products = sorted(
#         get_product_queryset(query), key=attrgetter('name'), reverse=True
#     )
#     print(products)
#     context['products'] = products
#     context['cart'] = cart

#     return render(request, template_name, context)


def create_product_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    if not user.is_manager:
        return HttpResponseNotFound("You're not allowed to view this page")

    form = CreateProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        last_editor = Account.objects.filter(email=user.email).first()
        obj.last_editor = last_editor
        obj.save()
        form = CreateProductForm()
        # return redirect(f'product/{obj.slug}')
        return redirect('product:all')

    context['form'] = form
    categories = []
    for cat in CATEGORIES:
        categories.append({
            'id': cat[0],
            'val': cat[1],
        })
    context['categories'] = categories
    return render(request, "product/create_product.html", context)


def detail_product_view(request, slug):

    context = {}
    cart = get_object_or_404(Cart, account=request.user)
    print(cart)
    product = get_object_or_404(Product, slug=slug)
    print(product)
    quantity = 1
    if request.POST:
        form = AddToCartForm(
            request.POST or None,
            request.FILES or None
        )
        if form.is_valid():
            cart_item = form.save(cart, product)
            form = AddToCartForm()

    form = AddToCartForm(initial={'quantity': quantity, })

    context['form'] = form
    context['product'] = product
    context['available'] = product.stock

    if product in cart.products.all():
        cart_item = CartItem.objects.get(product=product, cart=cart)
        context['quantity'] = cart_item.quantity
        context['available'] = product.stock - cart_item.quantity

    return render(request, 'product/detail_product.html', context)


def edit_product_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    if not user.is_manager:
        return HttpResponseNotFound("Unauthorized access.")

    product = get_object_or_404(Product, slug=slug)

    if request.POST:
        form = UpdateProductForm(
            request.POST or None, request.FILES or None, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            product = obj

    form = UpdateProductForm(
        initial={
            "name": product.name,
            "manufacturer": product.manufacturer,
            "category": product.category,
            "model": product.model,
            "price": product.price,
            "specifications": product.specifications,
            "stock": product.stock,
            "discount": product.discount,
        }
    )

    context['form'] = form

    categories = []
    for cat in CATEGORIES:
        categories.append({
            'id': cat[0],
            'val': cat[1],
        })

    context['categories'] = categories

    return render(request, 'product/edit_product.html', context)


def confirm_delete_product_view(request, slug):
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    if not user.is_manager:
        return HttpResponseNotFound("Unauthorized access.")

    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,
    }

    return render(request, "product/confirm_delete.html", context)


def delete_product_view(request, slug):
    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")
    if not user.is_manager:
        return HttpResponseNotFound("Unauthorized access.")

    product = get_object_or_404(Product, slug=slug)

    product.delete()

    return redirect("product:all")


def get_product_queryset(query=None):
    queryset_result = []
    queries = query.split(" ")  # python install 2019 = [python, install, 2019]
    for q in queries:
        products = Product.objects.filter(
            Q(name__contains=q) | Q(manufacturer__contains=q)
        ).distinct()
        for product in products:
            queryset_result.append(product)
    return list(set(queryset_result))
