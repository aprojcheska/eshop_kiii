"""
URL configuration for eshop_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from eshop_app.views import home, products, account, delivery, confirmation, ordered, cart, register, addproduct, add_to_cart, update_cart, remove_item, remove_product, favicon_view
from django.conf import settings
from django.conf.urls.static import static
#
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('products/', products, name="products"),
    path('account/', account, name="account"),
    path('delivery/', delivery, name="delivery"),
    path('confirmation/', confirmation, name="confirmation"),
    path('ordered/', ordered, name="ordered"),
    path('cart/', cart, name="cart"),
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('admin_account/', addproduct, name='addproduct'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_item/<int:item_id>/', remove_item, name='remove_item'),
    path('remove_product/<int:product_id>', remove_product, name="remove_product"),
    path('favicon.ico/', favicon_view),


re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

