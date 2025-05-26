from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ("name", "catalog", "price", "image_tag")
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="object-fit:contain;" />', obj.image.url)
        return "-"

    image_tag.short_description = "Изображение"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "catalog":
            kwargs["queryset"] = Catalog.objects.filter(parent__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Broadcast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "created_at", "sent_at")
    list_filter = ("status",)
    filter_horizontal = ("recipients",)
