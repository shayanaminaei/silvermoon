from rest_framework import serializers
from .models import Cart, OrderItem, Order
from productions.models import Product, Color


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'main_image']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']  # فقط فیلدهای مورد نیاز، در اینجا 'id' و 'name'


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    color = ColorSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'color', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    cartitem_set = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'identifier', 'cartitem_set']

    def get_cartitem_set(self, cart):
        cart_items = OrderItem.objects.filter(cart=cart)
        serializer = OrderItemSerializer(cart_items, many=True)
        return serializer.data


class OrderDetailSerializer(serializers.ModelSerializer):
    orderitem_set = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['address_id', 'user_id', 'orderitem_set']

    def get_orderitem_set(self, order):
        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data
