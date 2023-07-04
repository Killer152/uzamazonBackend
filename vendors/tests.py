from django.test import TestCase
from django.contrib.auth.models import User
from vendors.models import VendorModel


# Use this command : python manage.py test --keepdb

class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password="admin",
        )
        cls.vm = VendorModel.objects.create(
            user=cls.user, title="aaa", phone='111', website="a", instagram="b", description="yep", verified=True
        )

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_one(self):
        self.assertEqual(self.vm.user, self.user)
        self.assertEqual(self.vm.title, "aaa")
        self.assertEqual(self.vm.phone, "111")
        self.assertEqual(self.vm.website, "a")
        self.assertEqual(self.vm.instagram, "b")
        self.assertEqual(self.vm.description, "yep")
        self.assertEqual(self.vm.verified, True)
        self.assertEqual(self.vm.__str__(), "aaa | ")
