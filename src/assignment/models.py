from django.db import models
# Always aware of translations to other languages in the future -> wrap all static texts into _()
from django.utils.translation import ugettext_lazy as _


class UnicodeNameMixin(object):

    def __unicode__(self):
        return u"%s" % self.name


class Currency(UnicodeNameMixin, models.Model):
    """
    Default currency will be USD. All rates are USD based.
    """
    name = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        verbose_name_plural = _('Currencies')


class Fee(models.Model):
    """
    Fee model
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
    Product model
    """
    name = models.CharField(max_length=255)
    fee = models.ForeignKey(Fee, blank=True, null=True)


class Event(UnicodeNameMixin, models.Model):
    """
    Event model
    """
    name = models.CharField(max_length=255)
    # The sum of the fees can be slightly larger then single fee
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    fee = models.ForeignKey(Fee)

    products = models.ManyToManyField(Product, through='ProductItem')

    def get_products(self):
        return self.product_items.all().select_related('product__fee__currency')

class ProductItem(models.Model):
    """
    Intermediate model to store products quantity and relations.
    """
    product = models.ForeignKey(Product, related_name='items')
    event = models.ForeignKey(Event, related_name='product_items')

    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return u"%(name)s: %(quantity)s" % {
            'name': self.product.name,
            'quantity': self.quantity
        }




