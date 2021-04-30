"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# # Account imports
# from account.views import (
#     registrarion_view,
#     logout_view,
#     login_view,
#     account_view,
#     must_authenticate_view,
# )

# # Cart imports
# from cart.views import (
    
# )

# # Customer imports
# from customer.views import (
    
# )

# Personal imports
from personal.views import (
    home_screen_view
)


urlpatterns = [
    path('', home_screen_view, name='home'),
    path('admin/', admin.site.urls),
    path('product/', include('product.urls', 'product')),
]
