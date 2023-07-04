from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param


def get_next_link(request, page):
    if not page.has_next():
        return None
    url = request.build_absolute_uri()
    page_number = page.next_page_number()
    return replace_query_param(url, 'page', page_number)


def get_previous_link(request, page):
    if not page.has_previous():
        return None
    url = request.build_absolute_uri()
    page_number = page.previous_page_number()
    if page_number == 1:
        return remove_query_param(url, 'page')
    return replace_query_param(url, 'page', page_number)


def paginate(request, queryset, serializer, **kwargs):
    page_size = request.GET.get('page_size', 8)
    page = request.GET.get('page')
    paginator = Paginator(queryset, page_size)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    products = serializer(page, many=True, context={'request': request})
    data = {
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'next': get_next_link(request, page),
        'previous': get_previous_link(request, page),
        'products': products.data,
        'params': {}
    }
    for name, value in kwargs.items():
        data['params'][name] = value.data
    return Response(data=data, status=status.HTTP_200_OK)


def filter_products(request, products):
    sort_by = request.GET.get('sort_by')
    category = request.GET.get('category')
    product_type = request.GET.get('product_type')
    manufacturer = request.GET.get('manufacturer')
    max_price = request.GET.get('max_price')
    min_price = request.GET.get('min_price')
    stars = request.GET.get('stars')
    query = request.GET.copy()
    if category:
        category = query.pop('category')
        products = products.filter(category__id__in=category)
    if sort_by == 'expensive':
        products = products.order_by('-price')
    elif sort_by == 'cheap':
        products = products.order_by('price')
    if product_type:
        # product_type = query.pop('product_type')
        product_type = product_type.split(',')
        products = products.filter(product_type__id__in=product_type)
    if manufacturer:
        # manufacturer = query.pop('manufacturer')
        manufacturer = manufacturer.split(',')
        products = products.filter(manufacturer_id__in=manufacturer)
    if max_price and min_price:
        products = products.filter(price__range=(min_price, max_price))
    elif max_price:
        products = products.filter(price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    if stars:
        products = products.filter(rate__gte=stars)
    return products
