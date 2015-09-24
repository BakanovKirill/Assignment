from .models import Event, Product, ProductItem, Currency, Fee

__author__ = 'feanor'
"""
Django wrappers to customize admin interface a bit.
"""

from django.contrib import admin

class ProductInline(admin.TabularInline):
    model = ProductItem

class EventAdmin(admin.ModelAdmin):
    inlines = [ProductInline,]
    readonly_fields = ['total',]


admin.site.register(Event, EventAdmin)

admin.site.register(Product, list_display=('name', 'fee'))
admin.site.register(Currency, list_display=('name', 'rate'))

admin.site.register(ProductItem)
admin.site.register(Fee)

