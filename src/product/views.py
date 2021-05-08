from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from product.models import Product
from product.constants import CATEGORIES
from product.forms import CreateProductForm, UpdateProductForm
from account.models import Account


def get_all_products_view(request, slug=None):

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    if slug:
        product = get_object_or_404(Product, slug=slug)
        product.delete()

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product/list_products.html', context)


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
    product = get_object_or_404(Product, slug=slug)
    context['product'] = product

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
    queryset = []
    queries = query.split(" ")
    for q in queries:
        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(specifications__icontains=q)
        ).distinct()
        
        for product in products:
            queryset.append(product)
            
    return list(set(queryset))
