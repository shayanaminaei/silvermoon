from django.urls import path, re_path
from . import views
app_name = 'productions'

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
    path('zohoverify/verifyforzoho.html', views.zoho_verification, name='zoho'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('about/', views.AboutUs.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),
    re_path(r'^(?P<category_slug>[-\w\u0600-\u06FF]+)/$', views.ProductList.as_view(), name='product_list_by_category'),
    re_path(r'^(?P<id>[0-9]+)/(?P<slug>[-\w\u0600-\u06FF]+)/$', views.ProductDetail.as_view(), name='product_detail'),

]
