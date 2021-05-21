from django.urls import path
from .views import (
    CartListView,
    get_cart_detail_view,
    get_cart_customer_detail_view,
    add_product_to_cart_view,
    cart_add_product_detail_view,
)

app_name = 'carts'
urlpatterns = [
    path('', CartListView.as_view(), name='carts-list'),
    # path('create/', ArticleCreateView.as_view(), name='article-create'),
    # path('<int:id>/', CartDetailView.as_view(), name='cart-detail'),
    path(
        '<int:id>/purchase/',
        get_cart_customer_detail_view,
        name='cart-customer'
    ),
    path('<int:id>/', get_cart_detail_view, name='cart-detail'),
    path(
        '<int:id>/<int:p_id>',
        get_cart_detail_view,
        name='cart-detail-remove'
    ),
    path('<int:id>/add', add_product_to_cart_view, name='cart-add-product'),
    path(
        '<int:cart_id>/add/product/<int:product_id>',
        cart_add_product_detail_view,
        name='cart-add-product-detail'
    ),
]
