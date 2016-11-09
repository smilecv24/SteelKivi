import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.

from product.forms import CommentForm
from product.models import Product


def products(request):
    sort = request.GET.get('sort')
    if sort:
        products_list = Product.objects.prefetch_related('user_like').all()
        paginator = Paginator(products_list.order_by('-user_like'), 3)  # Show 1 contacts per page
    else:
        products_list = Product.objects.prefetch_related('user_like').all()
        paginator = Paginator(products_list, 3)  # Show 1 contacts per page

    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products_page = paginator.page(paginator.num_pages)
    return render(request, "products.html", {
        "products": products_page
    })


def product(request, product_detail, error=None):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    prod = Product.objects.prefetch_related('comment_set', 'user_like').get(slug=product_detail)
    return render(request, "product.html", {
        "product": prod,
        "comments": prod.comment_set.filter(created_at__gte=date_from),
        "form": CommentForm,
        "error": error
    })


def add_comment(request, product_slug):
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = Product.objects.get(slug=product_slug)
            form.save()
    return redirect('product', product_detail=product_slug)


def add_like(request, product_slug):
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    prod = Product.objects.prefetch_related('comment_set').filter(slug=product_slug)
    if request.user.is_authenticated():
        try:
            if prod.filter(user_like__in=[request.user]).count() > 0:
                return render(request, "product.html", {
                    "product": prod.first(),
                    "comments": prod.first().comment_set.filter(created_at__gte=date_from),
                    "form": CommentForm,
                    "error": "you already like it"
                })
            else:
                prod = prod.first()
                prod.user_like.add(request.user)
                prod.save()
        except ObjectDoesNotExist:
            raise Http404
        return redirect('product', product_detail=product_slug)
    else:
        return render(request, "product.html", {
            "product": prod.first(),
            "comments": prod.first().comment_set.filter(created_at__gte=date_from),
            "form": CommentForm,
            "error": "you are not authorised"
        })
