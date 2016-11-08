import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response

# Create your views here.

from product.models import Product


def products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 1)  # Show 1 contacts per page

    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products_page = paginator.page(paginator.num_pages)
    return render_to_response("products.html", {
        "products": products_page
    })


def product(request, product_detail):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    prod = Product.objects.prefetch_related('comment_set').get(slug=product_detail)
    return render_to_response("product.html", {
        "product": prod,
        "comments": prod.comment_set.filter(created_at__gte=date_from)
    })
