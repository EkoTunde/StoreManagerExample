from django.urls import path
from product.views import (
    create_product_view,
    detail_product_view,
    edit_product_view,
    get_all_products_view,
    confirm_delete_product_view,
    delete_product_view,
)

app_name = 'product'

urlpatterns = [
    path('', get_all_products_view, name="all"),
    path('create/', create_product_view, name="create"),
    path('<slug>/edit', edit_product_view, name="edit"),
    path('<slug>/confirm', confirm_delete_product_view, name="confirm"),
    path('<slug>/', detail_product_view, name="detail"),
    path('delete/', delete_product_view, name="delete"),
]
