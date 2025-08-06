from django.urls import path, re_path
from . import views
app_name = 'productions'

urlpatterns = [
    path('donate/', views.DonationView.as_view(), name='donation_form'),
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('zohoverify/verifyforzoho.html', views.zoho_verification, name='zoho'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    
    # Shop List URLs
    path('shop-list/', views.shop_list_view, name='shop_list'),
    path('shop-list/add/<int:product_id>/', views.add_to_shop_list, name='add_to_shop_list'),
    path('shop-list/remove/<int:product_id>/', views.remove_from_shop_list, name='remove_from_shop_list'),
    
    re_path(r'^(?P<category_slug>[-\w\u0600-\u06FF]+)/$', views.ProductList.as_view(), name='product_list_by_category'),
    re_path(r'^(?P<id>[0-9]+)/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.ProductDetail.as_view(), name='product_detail'),
    
]

