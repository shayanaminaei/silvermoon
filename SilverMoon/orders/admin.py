from django.contrib import admin
from .models import *


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product_id']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_address",)
    list_filter = ("full_address",)
    search_fields = ("full_address", "user_id__phone")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("address_id", "user_id", "paid")
    list_filter = ("user_id", "paid", "address_id")
    search_fields = ("address_id", "user_id")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_id", "price", "quantity")
    list_filter = ("product_id", "order")
    search_fields = ("order__id", "prodcut_id__name")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("identifier",)
    inlines = [OrderItemInline]
