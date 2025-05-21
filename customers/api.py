import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, authenticate, login, logout

from orders.models import Address, Cart
from .serializer import UserSerializer, UserProfileSerializer, AddressSerializer

User = get_user_model()


class RegisterApi(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginAPIView(APIView):
    def post(self, request):
        user = authenticate(phone=request.POST['phone'], password=request.POST['password'])
        login(request, user)
        return Response()


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        try:
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
        except jwt.ExpiredSignatureError:
            response = Response({'error': 'Access token has expired'}, status=401)
            response.delete_cookie('access_token')
            return response
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid access token'}, status=401)
        return Response(serializer.data)

    def get_user_object(self, pk):
        user = get_object_or_404(User, pk=pk)
        return user

    def put(self, request):
        access_token = request.COOKIES.get('access_token')
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        user = self.get_user_object(user_id)
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Logout(APIView):
    permission_classes = [IsAuthenticated]  # فقط کاربران احراز هویت‌شده بتوانند Logout کنند

    def post(self, request):
        response_data = {'message': 'Logout successful.', 'redirect_url': '/'}  # افزودن `redirect_url`

        identifier_ = request.COOKIES.get('cart_identifier')

        # حذف سبد خرید در صورت وجود
        if identifier_:
            try:
                cart = Cart.objects.get(identifier=identifier_)
                cart.delete()
            except Cart.DoesNotExist:
                pass

        # خروج کاربر و حذف کوکی‌ها
        logout(request)
        response = JsonResponse(response_data)  # استفاده از `response_data`
        response.delete_cookie('access_token')
        response.delete_cookie(settings.CART_COOKIE_NAME)
        response.delete_cookie('cart_identifier')  # حذف شناسه سبد خرید

        return response


def login_register_page(request):
    return render(request, 'login.html', {})


class AddressApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)  # اصلاح `user_id`
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = Address.objects.create(
            user_id=request.user,
            full_address=serializer.validated_data['full_address']
        )

        return Response({"message": "آدرس ذخیره شد!", "address_id": address.id}, status=201)


