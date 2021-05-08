from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView
)

from .forms import RawProductForm
from .models import Cart, CartItem


class CartListView(ListView):
    template_name = 'carts/carts_list.html'
    queryset = Cart.objects.all()


class CartDetailView(DetailView):
    template_name = 'carts/cart_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cart, id=id_)