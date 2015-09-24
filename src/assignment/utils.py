from decimal import Decimal
from django.db.models import F, Sum, DecimalField, ExpressionWrapper


def calculate_total_simple(event):
    """
    Simple loop based method to calculate total fee
    """
    product_items = event.product_items.select_related('product__fee__currency', 'event__fee__currency')
    summ = 0
    for item in product_items:
        fee = item.product.fee
        if not fee:
            fee = event.fee
        am = fee.amount
        rate = fee.currency.rate
        summ += am * rate * item.quantity
    return summ


def calculate_total_fast(event):
    """
    More elegant way to calculate fee total amount using builtin Django query expressions functions

    Makes 2 queries total but has less complexity.
    """
    product_items = event.product_items.select_related('product__fee__currency', 'event__fee__currency')
    product_items_with_fee = product_items.filter(product__fee__isnull=False)
    if product_items_with_fee:
        products_fee_amount = product_items_with_fee.aggregate(
            amount=Sum(ExpressionWrapper(F('product__fee__amount') * F('product__fee__currency__rate') * F('quantity'),
                                         output_field=DecimalField())))['amount']
    else:
        products_fee_amount = Decimal('0.0')
    products_without_fee = product_items.filter(product__fee__isnull=True)
    if products_without_fee:
        event_fee_amount = product_items.filter(product__fee__isnull=True).aggregate(
            amount=Sum(ExpressionWrapper(F('event__fee__amount') * F('event__fee__currency__rate') * F('quantity'),
                                         output_field=DecimalField())))['amount']
    else:
        event_fee_amount = Decimal('0.0')
    return products_fee_amount + event_fee_amount