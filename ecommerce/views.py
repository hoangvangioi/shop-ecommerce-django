from django.shortcuts import render
from store.models import Product, ReviewRating
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



# def home(request):
#     products = Product.objects.all().filter(is_available=True).order_by('created_date')
#     context = {
#         'products': products,
#     }
#     return render(request, 'store/store.html', context)

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
        'products': paged_products,
    }
    return render(request, 'home.html', context)


def error(request, exception,):
    return render(request, '404.html')


def handler500(request, *args, **argv):
    return render(request, '404.html', status=500)

def handler403(request, *args, **argv):
    return render(request, '404.html', status=403)


def csrf_failure(request, reason=""):
    return render(request, '404.html')