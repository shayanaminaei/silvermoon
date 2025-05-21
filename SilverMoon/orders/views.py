import uuid

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import CartAddProductForm, OrderForm
from productions.models import Product, Color
from .models import Cart, OrderItem, Order, Address
from .serializer import CartSerializer, OrderItemSerializer, OrderDetailSerializer
from django.conf import settings


# Create your views here.


import json
import base64


class UpdateCartItemView(APIView):
    def post(self, request):
        cart_identifier = request.COOKIES.get('cart_identifier')

        if not cart_identifier:
            return Response({'error': 'Cart not found'}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, identifier=cart_identifier)
        cart_data = request.data.get('cart', [])

        updated_prices = {}

        for item in cart_data:
            product_id = item.get('product_id')
            color_id = item.get('color_id')
            quantity = item.get('quantity')

            if product_id is None or quantity is None:
                continue

            cart_item = OrderItem.objects.filter(cart=cart, product_id=product_id, color_id=color_id).first()

            if cart_item:
                cart_item.quantity = quantity
                cart_item.save()
                updated_prices[f"{product_id}-{color_id}"] = cart_item.price  # فرمت داده برای دریافت صحیح در JS

        return Response({'success': 'Cart updated', 'prices': updated_prices}, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    def post(self, request):
        cart_identifier = request.COOKIES.get("cart_identifier")

        if not cart_identifier:
            return Response({"error": "سبد خرید یافت نشد!"}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, identifier=cart_identifier)
        cart.items.all().delete()  # حذف همه آیتم‌های سبد خرید

        return Response({"success": "سبد خرید با موفقیت حذف شد!"}, status=status.HTTP_200_OK)


class AddCartItemView(APIView):
    def post(self, request, product_id):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())

        product = get_object_or_404(Product, id=product_id)

        form = CartAddProductForm(request.POST, product=product)  # ارسال فرم با `product`

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            color = form.cleaned_data['color']  # اکنون `color` شیء کامل است

            cart, _ = Cart.objects.get_or_create(identifier=cart_identifier)
            cart.add_item(product, quantity, color)  # ارسال شیء `color`

            cart_serializer = CartSerializer(cart)
            response = Response(cart_serializer.data, status=status.HTTP_200_OK)
            response.set_cookie('cart_identifier', cart_identifier)
            return response
        else:
            return Response({'error': 'Invalid form', 'details': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CartRemoveItemView(APIView):

    def post(self, request, product_id):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())

        cart = Cart.objects.get_or_create(identifier=cart_identifier)
        cart = cart[0]
        product = get_object_or_404(Product, id=product_id)

        color_id = request.POST.get('color')
        # print('remove')
        # print(color_id)
        color = get_object_or_404(Color, id=color_id) if color_id else None
        # print(color)

        cart.remove_item(product, color)
        response = Response(status=200)
        response.set_cookie(settings.CART_COOKIE_NAME, '')
        return response


class CartDetail(APIView):
    """
        Detail of Cart
    """

    serializer_class = CartSerializer

    def get(self, request):
        cart_identifier = request.COOKIES.get('cart_identifier')
        if not cart_identifier:
            cart_identifier = str(uuid.uuid4())
        cart, _ = Cart.objects.get_or_create(identifier=cart_identifier)
        serializer = CartSerializer(cart)
        response = Response(serializer.data)
        response.set_cookie('cart_identifier', cart_identifier)
        return response


def show_cart(request):
    return render(request, 'cart.html', {})


# SHOW CHECKOUT HTML
def show_checkout(request):
    if not request.user.is_authenticated:
        return HttpResponse('ابتدا وارد شوید')

    form = OrderForm(request.POST or None, user=request.user)

    # دریافت مبلغ کل سبد خرید
    cart_identifier = request.COOKIES.get('cart_identifier')
    cart = Cart.objects.filter(identifier=cart_identifier).first()
    total_amount = 0
    if cart:
        total_amount = sum(item.price * item.quantity for item in OrderItem.objects.filter(cart=cart))

    context = {
        'form': form,
        'total_amount': total_amount  # ارسال مبلغ کل به checkout.html
    }
    return render(request, 'checkout.html', context)

#  ADD ORDER in DATABASE
class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address')

        # بررسی وجود آدرس و اینکه متعلق به کاربر است
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return Response({"error": "آدرس یافت نشد!"}, status=400)

        # ایجاد سفارش
        order = Order.objects.create(address_id=address, user_id=request.user)
        serializer = OrderDetailSerializer(order)

        # انتقال محصولات سبد خرید به سفارش
        cart_identifier = request.COOKIES.get('cart_identifier')
        cart = Cart.objects.get(identifier=cart_identifier)

        if not cart:
            return Response({"error": "سبد خرید خالی است!"}, status=400)

        order_items = OrderItem.objects.filter(cart=cart)
        for item in order_items:
            item.order = order
            item.save()

        # پاک کردن سبد خرید
        # cart.delete()

        response = Response(serializer.data)
        response.delete_cookie('mycart')
        response.delete_cookie('cart_identifier')
        return response


# PAID ORDER
class CheckOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = Order.objects.filter(user_id=request.user).order_by('id').last()
        order.paid = True
        order.save()
        return Response()


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)


class OrderDetailInfo(APIView):
    def get(self, request):
        html = render(request, 'order_detail.html')
        return Response({'html': html.content})
