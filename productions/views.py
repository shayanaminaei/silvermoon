from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Image, Category, Donation, ShopList
from .form import DonationForm
from orders.form import CartAddProductForm


# Create your views here.


class LandingPage(View):
    def get(self, request):
        last_5_products = Product.objects.order_by('-id')[:4]
        last_5_categories = Category.objects.order_by('-id')[:4]
        
        # Get accessories category products (پرفروش ترین اکسسوری ها)
        try:
            accessory_category = Category.objects.get(category_name__icontains='اکسسوری')
            accessory_products = Product.objects.filter(category=accessory_category, available=True).order_by('?')[:8]
        except Category.DoesNotExist:
            accessory_products = Product.objects.none()
        
        # Get random popular products (پربازدید ترین محصولات)
        popular_products = Product.objects.filter(available=True).order_by('?')[:8]
        
        context = {
            'products': last_5_products, 
            'categories': last_5_categories,
            'accessory_products': accessory_products,
            'popular_products': popular_products
        }
        return render(request, "landing_page.html", context)


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
    paginate_by = 9

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
    template_name = 'search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get("q")
        if not query:
            return Product.objects.none()
        
        # Search in both products and categories
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(specifications__icontains=query)
        ).distinct()
        
        return products
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        
        if query:
            # Search categories too
            categories = Category.objects.filter(
                Q(category_name__icontains=query)
            )
            
            context['categories_results'] = categories
            context['query'] = query
            
            # Check if no results found
            if not context['results'] and not categories:
                context['no_results'] = True
        
        return context


def zoho_verification(request):
    return render(request, 'verifyforzoho.html', {})



class DonationView(View):
    def get(self, request):
        form = DonationForm()
        return render(request, 'donation_form.html', {'form': form})

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'donation_success.html')
        return render(request, 'donation_form.html', {'form': form})


@login_required
@require_POST
def add_to_shop_list(request, product_id):
    """Add product to user's shopping list"""
    product = get_object_or_404(Product, id=product_id)
    
    # Try to create or get existing entry
    shop_item, created = ShopList.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': 'محصول با موفقیت به لیست خرید اضافه شد!',
            'action': 'added'
        })
    else:
        return JsonResponse({
            'success': True,
            'message': 'این محصول قبلاً در لیست خرید شما وجود دارد!',
            'action': 'exists'
        })


@login_required
@require_POST
def remove_from_shop_list(request, product_id):
    """Remove product from user's shopping list"""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        shop_item = ShopList.objects.get(user=request.user, product=product)
        shop_item.delete()
        return JsonResponse({
            'success': True,
            'message': 'محصول با موفقیت از لیست خرید حذف شد!',
            'action': 'removed'
        })
    except ShopList.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'این محصول در لیست خرید شما وجود ندارد!',
            'action': 'not_found'
        })


@login_required
def shop_list_view(request):
    """Display user's shopping list"""
    shop_items = ShopList.objects.filter(user=request.user).select_related('product')
    
    context = {
        'shop_items': shop_items,
        'total_items': shop_items.count()
    }
    
    return render(request, 'shop_list.html', context)
