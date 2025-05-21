import uuid

from django.db import models
from productions.models import Product, Color
from customers.models import User
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Address(models.Model):
    full_address = models.TextField(_("آدرس ارسالی"), max_length=100)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("کاربر"))

    class Meta:
        verbose_name = _('آدرس')
        verbose_name_plural = _('آدرس ها')

    def __str__(self):
        # return str(self.user_id)
        return f"{self.full_address}"


class Order(BaseModel):
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name=_("آدرس"))
    paid = models.BooleanField(verbose_name=_("پرداخت شده"), default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("کاربر"))

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارش ها')

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class Cart(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def add_item(self, product, quantity=1, color=None):
        cart_item, created = OrderItem.objects.get_or_create(
            cart=self,
            product_id=product,  # استفاده از product_id به جای product
            color=color,
            defaults={'quantity': quantity, 'price': product.price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_item(self, product, color=None):
        print('what is the color?')
        print(color)
        try:
            if color:
                cart_item = OrderItem.objects.get(cart=self, product_id=product, color=color)
            else:
                cart_item = OrderItem.objects.get(cart=self, product_id=product)  # در غیر این صورت بر اساس فقط محصول
            cart_item.delete()
        except OrderItem.DoesNotExist:
            pass

    def get_total_quantity(self):
        return self.cartitem_set.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    def get_total_price(self):
        return self.cartitem_set.annotate(total_price=models.F('quantity') * models.F('product__price')) \
            .aggregate(total_price=models.Sum('total_price'))['total_price'] or 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, verbose_name=_("مربوط به سفارش"), null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("محصول"))
    price = models.PositiveIntegerField(_("قیمت"))
    quantity = models.PositiveIntegerField(_("تعداد"), default=0)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_('رنگ'))  # اصلاح فیلد رنگ به ForeignKey

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('آیتم سفارش')
        verbose_name_plural = _('آیتم های سفارش')

    def get_cost(self):
        return self.quantity * self.price

