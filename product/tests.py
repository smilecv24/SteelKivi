from django.test import TestCase, Client

# Create your tests here.
from product.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Product.objects.create(name='TestProduct', slug='test', description='About test product', price=1.1)

    def testModel(self):
        product = Product.objects.first()
        self.assertEqual(product.__str__(), product.name)

    def testUrls(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/test/')
        self.assertEqual(response.status_code, 200)
