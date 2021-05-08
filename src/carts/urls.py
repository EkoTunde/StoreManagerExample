from django.urls import path
from .views import (
    CartListView,
)

app_name = 'carts'
urlpatterns = [
    path('', CartListView.as_view(), name='carts-list'),
    # path('create/', ArticleCreateView.as_view(), name='article-create'),
    # path('<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    # path('<int:id>/update/', ArticleUpdateView.as_view(), name='article-update'),
    # path('<int:id>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
]