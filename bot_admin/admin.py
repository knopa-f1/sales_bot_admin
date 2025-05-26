from django.contrib import admin

from .models import User, Cart, Order, OrderItem, Catalog, Product

admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
