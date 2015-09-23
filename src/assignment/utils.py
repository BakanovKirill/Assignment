from django.db.models import F, Sum


def calculate_total_simple(event):
    product_items = event.product_items.select_related('product__fee__currency', 'event__fee__currency')
    summ = 0
    for item in product_items:
        fee = item.product.fee
        if not fee:
            fee = event.fee
        am = fee.amount
        rate = fee.currency.rate
        summ += am * rate
    return summ


def calculate_total_fast(event):
    product_items = event.product_items.select_related('product__fee__currency', 'event__fee__currency')
    products_fee_amount = product_items.aggregate(
        amount=Sum(F('product__fee__amount') * F('product__fee__currency__rate')))['amount']
    event_fee_amount = product_items.filter(product__fee__isnull=True).aggregate(
        amount=Sum(F('event__fee__amount') * F('event__fee__currency__rate')))['amount']
    return products_fee_amount + event_fee_amount