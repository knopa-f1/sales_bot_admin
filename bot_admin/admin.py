from django.contrib import admin

from .models import User, Cart, Order, OrderItem, Catalog, Product, Broadcast

admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")

    def save_model(self, request, obj, form, change):
        if obj.parent and obj.parent.parent:
            raise ValueError("Доступны только 2 уровня вложенности категорий.")
        super().save_model(request, obj, form, change)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "catalog", "price")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "catalog":
            from .models import Catalog
            kwargs["queryset"] = Catalog.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "sent_at")
    list_filter = ("status",)
    filter_horizontal = ("recipients",)
