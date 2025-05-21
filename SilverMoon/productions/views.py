from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Image, Category
from orders.form import CartAddProductForm


# Create your views here.


class LandingPage(View):
    def get(self, request):
        last_5_products = Product.objects.order_by('-id')[:4]
        last_5_categories = Category.objects.order_by('-id')[:4]
        return render(request, "landing_page.html", {'products': last_5_products, 'categories': last_5_categories})


class AboutUs(View):
    def get(self, request):
        return render(request, "about.html", {})


class Contact(View):
    def get(self, request):
        return render(request, "contact.html", {})


class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 4

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count('product'))


# def product_list(request):
#     products = Product.objects.select_related('category').get(id=5)
#     return render(request, 'list.html', {"request": request, "products": products})


class ProductList(ListView):
    model = Product
    template_name = 'list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        print(category_slug)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            print('heloooooo')
            print(category_slug)
            queryset = queryset.filter(category=category)

        return queryset
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = context['object_list']
        for product in object_list:
            product.price = '{:20,.0f}'.format(product.price)
            context['categories'] = Category.objects.all()
        if object_list:
            context['form'] = CartAddProductForm(product=object_list[0])  # یک محصول نمونه برای ساخت فرم
        else:
            context['form'] = None  # یا یک فرم بدون مقدار محصول بساز
        return context



class ProductDetail(DetailView):
    model = Product
    template_name = 'detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # دریافت محصول

        context['images'] = Image.objects.filter(product_id=product.id)
        context['product'].price = '{:20,.0f}'.format(context['product'].price)
        context['form'] = CartAddProductForm(product=product)  # ارسال محصول صحیح
        context['categories'] = Category.objects.all()

        return context


class SearchResultsView(ListView):
    model = Product
    template_name = 'list.html'
    context_object_name = 'products'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Product.objects.filter(
            Q(name__icontains=query)
        )
        return object_list


def zoho_verification(request):
    return render(request, 'verifyforzoho.html', {})
