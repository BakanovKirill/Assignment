from decimal import Decimal
from django.db import models
# Always aware of translations to other languages in the future -> wrap all static texts into _()
from django.utils.translation import ugettext_lazy as _


class UnicodeNameMixin(object):
    """
    Simple mixin to show model names in default representation.
    """
    def __unicode__(self):
        """change this method to __str__ in Python >= 3.0"""
        return u"%s" % self.name


class Currency(UnicodeNameMixin, models.Model):
    """
    Default currency will be USD. All rates are USD based.

        - **name** -- currency international short name, i.e. USD, UAH etc.
        - **rate** -- rate in decimal. Rates are based on exchange to USD. USD itself has 1.00 rate.
         So if the currency is EUR, we need EUR to USD rate = 1.12 (on 24.09.2015).
    """
    name = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=6, decimal_places=4, help_text="USD based rate. USD itself has 1.00 rate")

    class Meta:
        verbose_name_plural = _('Currencies')


class Fee(models.Model):
    """
    Fee to apply to each Product in Event.

        - **amount** -- fee absolute amount in decimal.
        - **currency** -- currency in which fee is created. Used to calculate amount in USD.

    >>> currency_instance, created = Currency.objects.get_or_create(name='USD', rate=Decimal('1.0'))
    >>> fee_obj, created = Fee.objects.get_or_create(amount=Decimal('1.0'),currency=currency_instance)
    >>> fee_obj
    <Fee: 1.00 USD>
    """
    # Lets assume 999 999.99 is the max fee
    amount = models.DecimalField(max_digits=8, decimal_places=2, help_text=_("Default amount in USD"))
    currency = models.ForeignKey(Currency)

    class Meta:
        verbose_name = _('Service fee')

    def __unicode__(self):
        """ Small verbosity added """
        return u"%(amount)s %(currency)s" % {
            'amount': self.amount,
            'currency': self.currency.name
        }


class Product(UnicodeNameMixin, models.Model):
    """
    Products for adding to events

        - **name** -- product name
        - **fee** -- Fee instance. If not present, Event fee is applied

    >>> product, created = Product.objects.get_or_create(name='Chinese Phone')
    >>> product
    <Product: Chinese Phone>
    """
    name = models.CharField(max_length=255)
    fee = models.ForeignKey(Fee, blank=True, null=True)


class Event(UnicodeNameMixin, models.Model):
    """
    Events which store products

        - **name** -- name of event
        - **total** -- total fee amount
        - **fee** -- Fee which is applied to Product instance if no product.fee is present
        - **products** -- list of products for the event

    >>> currency_instance, created = Currency.objects.get_or_create(name='USD', rate=Decimal('1.0'))
    >>> fee_instance, created = Fee.objects.get_or_create(amount=Decimal('1.0'),currency=currency_instance)
    >>> event, created = Event.objects.get_or_create(name='Test event', fee = fee_instance)
    >>> event
    <Event: Test event>
    """
    name = models.CharField(max_length=255)
    # The sum of the fees can be slightly larger then single fee
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    fee = models.ForeignKey(Fee)

    products = models.ManyToManyField(Product, through='ProductItem')

    def get_products(self):
        """Returns preloaded product_items query to optimize preformance"""
        return self.product_items.all().select_related('product__fee__currency')


class ProductItem(models.Model):
    """
    ManyToMany "through" model to store products quantity.

        - **product** -- foreign key to Product
        - **event** -- foreign key to Event
        - **quantity** - amount of products of the same type
    """

    product = models.ForeignKey(Product, related_name='items')
    event = models.ForeignKey(Event, related_name='product_items')

    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u"%(name)s: %(quantity)s" % {
            'name': self.product.name,
            'quantity': self.quantity
        }




