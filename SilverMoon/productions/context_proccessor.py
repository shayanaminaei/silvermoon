from .models import Category


def categories(request):
    return {'categories_context': Category.objects.all(), }
