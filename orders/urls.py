from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.show_cart, name='cart'),
    path('detail/', views.CartDetail.as_view(), name='cart_api'),
    path('add/<int:product_id>/', views.AddCartItemView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', views.CartRemoveItemView.as_view(), name='cart_remove'),
    path('checkout/', views.show_checkout, name='checkout'),
    path('final/', views.OrderAPIView.as_view(), name='final'),
    path('paid/', views.CheckOut.as_view(), name='paid'),
    path('update/', views.UpdateCartItemView.as_view(), name='cart_update'),  # مسیر جدید برای بروزرسانی سبد خرید
    path('clear/', views.ClearCartView.as_view(), name='cart_clear'),  # مسیر جدید برای حذف کل سبد خرید
]
