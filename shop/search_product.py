from re import search as poisk


def filter_product(search, product):
    for a in product:
        a1 = False
        a2 = False
        a3 = False
        a4 = False
        if a.title_ru is not None:
            if poisk(search, a.title_ru.lower()):
                a1 = True
        if a.title_en is not None:
            if poisk(search, a.title_en.lower()):
                a2 = True
        if a.title_uz is not None:
            if poisk(search, a.title_uz.lower()):
                a3 = True
        try:
            if a.manufacturer.title:
                if poisk(search, a.manufacturer.title.lower()):
                    a4 = True
                if a1 is False and a2 is False and a3 is False and a4 is False:
                    product = product.exclude(title_ru=a.title_ru)
        except AttributeError:
            if a1 is False and a2 is False and a3 is False and a4 is False:
                product = product.exclude(title_ru=a.title_ru)
    return product


def search_product(search, queryset):
    words = len(search.split())
    split = search.split()
    for word in range(words):
        search = split[word]
        queryset = filter_product(search, queryset)
    return queryset
