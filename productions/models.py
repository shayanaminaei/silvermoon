from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(verbose_name=_('نام'), max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    photo = models.ImageField(verbose_name=_('عکس'), null=True, blank=True, upload_to='productions/')

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name, allow_unicode=True)
        super().save()

    def get_absolute_url(self):
        return reverse("productions:product_list_by_category", args=[self.slug])

    def __str__(self):
        return self.category_name


class Color(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = _('رنگ')
        verbose_name_plural = _('رنگ ها')

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(verbose_name=_('نام'), max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    brand = models.CharField(verbose_name=_('برند'), max_length=255)
    specifications = models.CharField(verbose_name=_('مشخصات'), max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('دسته بندی'))
    price = models.IntegerField(verbose_name=_('قیمت'))
    available = models.BooleanField(verbose_name=_('موجودی'), default=True)
    main_image = models.ImageField(verbose_name=_('عکس'), upload_to='productionss/')
    secondary_image = models.ImageField(null=True, blank=True, verbose_name=_('عکس'), upload_to='productionss/')
    colors = models.ManyToManyField(Color, verbose_name=_('رنگ‌ها'))

    class Meta:
        ordering = ('name',)
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("productions:product_detail", args=[self.id, self.slug])

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(verbose_name=_('نام'), max_length=255)
    product_id = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE, verbose_name=_('محصول'))
    photo = models.ImageField(verbose_name=_('عکس'), upload_to='productions/')

    class Meta:
        verbose_name = _('عکس')
        verbose_name_plural = _('عکس ها')

    def __str__(self):
        return self.name
