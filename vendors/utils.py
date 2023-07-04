import io
from re import search as poisk

import math
import pandas as pd
import xlsxwriter
from rest_framework import status
from rest_framework.response import Response

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView

from shop.models import ProductModel, CategoryModel, SubCategoryModel, ProductTypeModel, \
    ManufacturerModel, CountStatusModel
from vendors.permissions import VendorPermission
import unidecode
from unidecode import unidecode


class ExampleExportView(APIView):
    permission_classes = [VendorPermission]

    def get(self, request):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        data = ['Название', 'Title', 'Ismi', 'Description', 'Описание', 'Tavsif',
                'Characteristics', 'Характеристики', 'Xususiyatlari', 'Price/Цена/Narx',
                'Product type/Тип продукта/Mahsulot turi', 'Category/Категория/Turkum',
                'Subcategory/Подкатегория/Subkategoriyasi', 'Manufacturer/Производитель/Ishlab chiqaruvchi',
                'Quantity/Количество/Miqdor']
        data2 = ['Yamaha C340', 'Yamaha C340', 'Yamaha C340', 'Гитара из Польши', 'Guitar from Poland',
                 'Polshadan Gitarasi',
                 '6 струн', '6 strings', '6 strunlar', '150', 'Гитара', 'Музыкальные инструменты',
                 'Струнные инструменты', 'Yamaha', '4']
        g = 0
        for i in data:
            fll = len(i)
            worksheet.write(0, g, i)
            worksheet.set_column(g, g, fll + 3)
            g += 1
        g = 0
        for i in data2:
            worksheet.write(1, g, i)
            g += 1
        workbook.close()
        output.seek(0)
        filename = 'Example.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


class EmployeeImportView(APIView):
    permission_classes = [VendorPermission]

    def slug(self, title):
        slug = title
        if ProductModel.objects.filter(slug=slug).exists():
            slug = list(ProductModel.objects.get(slug=slug).slug)
            try:
                slug[-1] = str(int(slug[-1]) + 1)
                slug = "".join(slug)
                return self.slug(title=slug)
            except ValueError:
                slug = "".join(slug)
                slug = slug + str(1)
                return self.slug(title=slug)
        return slug

    def post(self, request):
        try:
            if self.request.FILES['import']:
                df = pd.read_excel(self.request.FILES['import'], engine='openpyxl')
                products = df.to_dict(orient='record')
                vendor = self.request.user.vendor
                for i in products:
                    title_ru = i["Название"]
                    title_en = i["Title"]
                    title_uz = i["Ismi"]
                    if type(title_ru) == str and title_ru != '':
                        slug = self.slug(unidecode(title_ru))
                    else:
                        return Response({"Fail": "Russian title is mandatory"}, status=status.HTTP_400_BAD_REQUEST)
                    if type(title_en) != str:
                        title_en = ' '
                    if type(title_uz) != str:
                        title_uz = ' '
                    description_ru = i["Описание"]
                    description_uz = i["Tavsif"]
                    description_en = i["Description"]
                    if type(description_ru) != str:
                        return Response({"Fail": "Russian description is mandatory"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if type(description_en) != str:
                        description_en = ' '
                    if type(description_uz) != str:
                        description_uz = ' '
                    characteristics_ru = i["Характеристики"]
                    characteristics_uz = i["Xususiyatlari"]
                    characteristics_en = i["Characteristics"]
                    if type(characteristics_ru) != str:
                        return Response({"Fail": "Russian characteristic is mandatory"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    if type(characteristics_uz) != str:
                        characteristics_uz = ' '
                    if type(characteristics_en) != str:
                        characteristics_en = ' '
                    price = i["Price/Цена/Narx"]
                    if type(price) != int and type(price) != float:
                        return Response({"Fail": "No price"}, status=status.HTTP_400_BAD_REQUEST)
                    elif math.isnan(price):
                        return Response({"Fail": "No price"}, status=status.HTTP_400_BAD_REQUEST)
                    count = i["Quantity/Количество/Miqdor"]
                    if type(count) != int:
                        return Response({"Fail": "No count"}, status=status.HTTP_400_BAD_REQUEST)
                    elif math.isnan(count):
                        return Response({"Fail": "No count"}, status=status.HTTP_400_BAD_REQUEST)
                    category2 = i["Category/Категория/Turkum"]
                    if type(category2) != str:
                        return Response({"Fail": "No category"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        a1 = False
                        for d in CategoryModel.objects.all():
                            if poisk(category2.lower(), d.title_ru.lower()):
                                category = d
                                a1 = True
                        if not a1:
                            return Response({"Fail": "No such category"}, status=status.HTTP_400_BAD_REQUEST)
                    subcategory2 = i["Subcategory/Подкатегория/Subkategoriyasi"]
                    if type(subcategory2) != str:
                        return Response({"Fail": "No subcategory"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        a2 = False
                        for d in SubCategoryModel.objects.all():
                            if poisk(subcategory2.lower(), d.title_ru.lower()):
                                subcategory = d
                                if subcategory.category != category:
                                    return Response({"Fail": "This subcategory is not connected to this category"},
                                                    status=status.HTTP_400_BAD_REQUEST)
                                a2 = True
                        if not a2:
                            return Response({"Fail": "No such subcategory"}, status=status.HTTP_400_BAD_REQUEST)
                    product_type2 = i["Product type/Тип продукта/Mahsulot turi"]
                    if type(product_type2) == str and title_ru != '':
                        a3 = False
                        for d in ProductTypeModel.objects.all():
                            if poisk(product_type2.lower(), d.title_ru.lower()):
                                product_type = d
                                if product_type.subcategory != subcategory:
                                    return Response({"Fail": "This product type is not connected to this subcategory"},
                                                    status=status.HTTP_400_BAD_REQUEST)
                                a3 = True
                        if not a3:
                            return Response({"Fail": "No such product type"}, status=status.HTTP_400_BAD_REQUEST)
                    elif type(product_type2) != str:
                        if type(product_type2) == int or type(product_type2) == float:
                            if math.isnan(product_type2):
                                product_type = None
                            else:
                                return Response({"Fail": "Wrong product type input"},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"Fail": "Wrong product type input"}, status=status.HTTP_400_BAD_REQUEST)
                    manufacturer2 = i["Manufacturer/Производитель/Ishlab chiqaruvchi"]
                    if type(manufacturer2) == str and manufacturer2 != '':
                        a4 = False
                        for d in ManufacturerModel.objects.all():
                            if poisk(manufacturer2.lower(), d.title.lower()):
                                manufacturer = d
                                if manufacturer.subcategory != subcategory or manufacturer.category != category:
                                    return Response(
                                        {"Fail": "This manufacturer is not connected to this subcategory/category"},
                                        status=status.HTTP_400_BAD_REQUEST)
                                a4 = True
                        if not a4:
                            return Response({"Fail": "No such manufacturer"}, status=status.HTTP_400_BAD_REQUEST)
                    elif type(manufacturer2) != str:
                        if type(manufacturer2) == int or type(manufacturer2) == float:
                            if math.isnan(manufacturer2):
                                manufacturer = None
                            else:
                                return Response({"Fail": "Wrong manufacturer type input"},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"Fail": "Wrong manufacturer type input"},
                                            status=status.HTTP_400_BAD_REQUEST)
                    pm = ProductModel.objects.create(title_ru=title_ru, title_en=title_en, title_uz=title_uz, slug=slug,
                                                     description_en=description_en, description_ru=description_ru,
                                                     description_uz=description_uz, image='import/default.png',
                                                     price=price, manufacturer=manufacturer, category=category,
                                                     characteristics_en=characteristics_en, subcategory=subcategory,
                                                     characteristics_uz=characteristics_uz, product_type=product_type,
                                                     characteristics_ru=characteristics_ru, vendor=vendor, count=count
                                                     )
                    CountStatusModel.objects.create(product=pm, count=count)
                    return Response({"Success": "Products were imported"}, status=status.HTTP_201_CREATED)
                return Response({"Fail": "No data"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Fail": "Wrong params key"}, status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return Response({"Fail": "Wrong params key"}, status=status.HTTP_400_BAD_REQUEST)
