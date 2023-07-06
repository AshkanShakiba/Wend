import string
import random
import datetime
from django.test import TestCase
from django.urls import reverse

from .models import Product, Order


class PagesTests(TestCase):
    def test_home_page_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)  # redirect

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)  # redirect

    def test_idle_page_view(self):
        response = self.client.get("/idle")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "idle.html")

        response = self.client.get(reverse("idle"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "idle.html")

    def test_select_page_view(self):
        response = self.client.get("/select")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "select.html")

        response = self.client.get(reverse("select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "select.html")

    def test_about_page_view(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")


class ModelsTests(TestCase):
    def test_product_model_create(self):
        name_len = random.randrange(1, 256)
        name = "".join(random.choices(string.ascii_letters, k=name_len))
        price = random.randrange(1, 4096)
        Product.objects.create(name=name, price=price)
        product = Product.objects.last()
        self.assertIsNotNone(product)
        self.assertEqual(product.name, name)
        self.assertEqual(str(product), name)
        self.assertEqual(len(product.name), name_len)
        self.assertEqual(product.price, price)

    def test_order_model_create(self):
        products_count = random.randrange(1, 9)
        for _ in range(products_count):
            name_len = random.randrange(1, 256)
            name = "".join(random.choices(string.ascii_letters, k=name_len))
            price = random.randrange(1, 4096)
            Product.objects.create(name=name, price=price)
        product = Product.objects.all()[random.randrange(products_count)]
        Order.objects.create(product=product)
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.product, product)
        self.assertEqual(str(order), f"{order.product} ({order.date})")
        self.assertIsNotNone(order.date)
        self.assertLessEqual(order.date, datetime.datetime.now(datetime.timezone.utc))


class ProductsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        products = []
        products_count = random.randrange(1, 9)
        for _ in range(products_count):
            name_len = random.randrange(1, 256)
            name = "".join(random.choices(string.ascii_letters, k=name_len))
            price = random.randrange(1, 4096)
            products.append(Product.objects.create(name=name, price=price))
        cls.products = products

    def test_select_view(self):
        response = self.client.get(reverse("select"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "select.html")
        for product in self.products:
            self.assertContains(response, product.name)


class OrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        name_len = random.randrange(1, 256)
        name = "".join(random.choices(string.ascii_letters, k=name_len))
        price = random.randrange(1, 4096)
        cls.product = Product.objects.create(name=name, price=price)

    def test_order_view(self):
        response = self.client.get(reverse("order", args=(self.product.id,)))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.product, self.product)
        self.assertEqual(str(order), f"{order.product} ({order.date})")
        self.assertIsNotNone(order.date)
        self.assertLessEqual(order.date, datetime.datetime.now(datetime.timezone.utc))
