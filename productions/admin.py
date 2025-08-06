from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ("category_name")
    search_fields = ("category_name__startswith",)

    fieldsets = (
        (None, {"fields": ("category_name", "photo")}),
    )


@admin.register(Color)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available")
    list_filter = ("category", "available", "price")
    search_fields = ("category__category_name",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("name", "product_id")
    list_filter = ("product_id",)
    search_fields = ("product_id",)



@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'created_at']