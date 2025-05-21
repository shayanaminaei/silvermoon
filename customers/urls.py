from django.urls import path
from . import api

app_name = 'customers'

urlpatterns = [
    path('api/register/', api.RegisterApi.as_view(), name="register"),
    path('api/login/', api.LoginAPIView.as_view(), name='login'),
    path('', api.login_register_page, name='login_register_page'),
    path('profile/', api.Profile.as_view(), name='profile'),
    path('logout/', api.Logout.as_view(), name='logout'),
    path('address/', api.AddressApi.as_view(), name='address'),
]
