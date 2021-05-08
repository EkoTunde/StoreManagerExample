from django.shortcuts import render
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
from .models import Cart


class CartListView(ListView):
    template_name = 'carts/carts_list.html'
    queryset = Cart.objects.all() # <blog>/<modelname>_list.html