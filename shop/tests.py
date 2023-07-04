from django.test import TestCase
from django.contrib.auth.models import User

# Use this command : python manage.py test --keepdb
from shop.models import CategoryModel, SubCategoryModel, ProductTypeModel, ManufacturerModel, ProductModel


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password="admin",
        )
        cls.tgm = CategoryModel.objects.create(title="title", slug="slug")
        cls.stgm = SubCategoryModel.objects.create(title="title", slug="slug", category=CategoryModel.objects.get())
        cls.ptm = ProductTypeModel.objects.create(title="title", slug="slug",
                                                  subcategory=SubCategoryModel.objects.get())
        cls.man = ManufacturerModel.objects.create(title="title", slug="slug",
                                                   subcategory=SubCategoryModel.objects.get(),
                                                   category=CategoryModel.objects.get())
        # cls.pm = ProductModel.objects.create(product_type=ProductTypeModel.objects.get(),
        #                                      category=CategoryModel.objects.get(),
        #                                      subcategory=SubCategoryModel.objects.get(),
        #                                      manufacturer=ManufacturerModel.objects.get(), title="title", slug="slug", )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_CategoryModel(self):
        self.assertEqual(self.tgm.title, "title")
        self.assertNotEqual(self.tgm.title, "aaa")
        self.assertEqual(self.tgm.slug, "slug")
        self.assertNotEqual(self.tgm.slug, "aaa")
        self.assertEqual(self.tgm.__str__(), "title")
        self.assertNotEqual(self.tgm.__str__(), "aaa")

    def test_SubCategoryModel(self):
        self.assertEqual(self.stgm.title, "title")
        self.assertNotEqual(self.stgm.title, "aaa")
        self.assertEqual(self.stgm.slug, "slug")
        self.assertNotEqual(self.stgm.slug, "aaa")
        self.assertEqual(self.stgm.category.title, "title")
        self.assertNotEqual(self.stgm.category.title, "aaa")
        self.assertEqual(self.stgm.__str__(), "title | title")
        self.assertNotEqual(self.stgm.__str__(), "aaa")

    def test_ProductTypeModel(self):
        self.assertEqual(self.ptm.title, "title")
        self.assertNotEqual(self.ptm.title, "aaa")
        self.assertEqual(self.ptm.slug, "slug")
        self.assertNotEqual(self.ptm.slug, "aaa")
        self.assertEqual(self.ptm.subcategory.title, "title")
        self.assertNotEqual(self.ptm.subcategory.title, "aaa")
        self.assertEqual(self.ptm.__str__(), "title | title")
        self.assertNotEqual(self.ptm.__str__(), "aaa")

    def test_ManufacturerModel(self):
        self.assertEqual(self.man.title, "title")
        self.assertNotEqual(self.man.title, "aaa")
        self.assertEqual(self.man.slug, "slug")
        self.assertNotEqual(self.man.slug, "aaa")
        self.assertEqual(self.man.subcategory.title, "title")
        self.assertNotEqual(self.man.subcategory.title, "aaa")
        self.assertEqual(self.man.category.title, "title")
        self.assertNotEqual(self.man.category.title, "aaa")
        self.assertEqual(self.man.__str__(), "title")
        self.assertNotEqual(self.man.__str__(), "aaa")
