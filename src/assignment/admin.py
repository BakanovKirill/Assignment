from .models import Event, Product, ProductItem, Currency, Fee

__author__ = 'feanor'

from django.contrib import admin


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(Product)
admin.site.register(Fee)
admin.site.register(Currency, list_display=('short_name', 'name', 'rate'))
admin.site.register(ProductItem)
