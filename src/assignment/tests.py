from decimal import Decimal

from django.test import TestCase

from assignment.models import Event, Currency, Fee, Product, ProductItem
from assignment.utils import calculate_total_simple, calculate_total_fast


class EventTestCase(TestCase):
    def setUp(self):
        self.usd = Currency.objects.create(name='USD', rate=Decimal('1.0'))
        self.gbp = Currency.objects.create(name='GBP', rate=Decimal('1.50'))

        self.fee_usd = Fee.objects.create(amount=Decimal('2.00'), currency=self.usd)
        self.fee_gbp = Fee.objects.create(amount=Decimal('2.00'), currency=self.gbp)

        self.book = Product.objects.create(name='Book')
        self.table = Product.objects.create(name='Table', fee=self.fee_gbp)
        self.sofa = Product.objects.create(name='Sofa', fee=self.fee_usd)

        self.event = Event.objects.create(name='Library meeting', fee=self.fee_usd)

        self.items = []
        for i, product in enumerate([self.book, self.sofa, self.table]):
            self.items.append(ProductItem.objects.create(event=self.event, product=product, quantity=i))

    def test_events(self):
        self.assertTrue(self.usd in Currency.objects.all())
        self.assertTrue(self.event in Event.objects.all())
        self.assertTrue(self.fee_gbp in Fee.objects.all())
        self.assertTrue(self.book in Product.objects.filter(name='Book'))
        self.assertTrue(self.items[0] in ProductItem.objects.all())

        self.assertEqual(self.sofa, self.event.products.get(name='Sofa'))

        total_fast = calculate_total_fast(self.event)
        total_simple = calculate_total_simple(self.event)

        self.assertEqual(total_fast,total_simple)