from django.shortcuts import render
from django.http import HttpResponse
from .models import Coffee
from cart.forms import CartAddProductForm
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404, render
# from .utils import q_search

def home(request):
    coffee = Coffee.objects.all()
    return render(request, 'home.html', {'coffee':coffee})

def _detail(request, id, slug):
    Coffee = get_object_or_404(Coffee, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'Coffee': Coffee})


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    
    if category_slug == "all":
        goods = Coffee.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Coffee.objects.filter(category__slug=category_slug))

   
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    context = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug
    }
    return render(request, "home.html", context)


def product(request, product_slug):
    product = Coffee.objects.get(slug=product_slug)

    context = {"Coffee": product}

    return render(request, "home.html", context=context)