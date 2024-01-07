from django.contrib import admin
from .models import Product, CustomUser, Cart, CartItem
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(Product, ProductAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')


admin.site.register(CartItem, CartItemAdmin)

