from django import template

register = template.Library()

COLOR_MAP = {
    "قرمز": "red",
    "آبی": "blue",
    "سبز": "green",
    "زرد": "yellow",
    "مشکی": "black",
    "سفید": "white",
    "خاکستری": "gray",
    "نارنجی": "orange",
    "بنفش": "purple",
    "صورتی": "pink",
    "قهوه‌ای": "brown"
}


@register.filter(name='translate_color')
def translate_color(color_name):
    """تبدیل نام رنگ فارسی به انگلیسی برای استفاده در CSS"""
    return COLOR_MAP.get(color_name, "gray")  # پیش‌فرض "gray" در صورت نبود رنگ
