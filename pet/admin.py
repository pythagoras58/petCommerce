"""
Django provides an inbuilt admin panel from which data can be directly managed
this admin.py will be used to manage the django admin site
"""
from django.contrib import admin
from .models import (
    Item,
    OrderItem,
    Order,
    Variation,
    ItemVariation
)


# Admin Classese
class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

# display list for pet display
    list_display = [
        'title',
        'price',
        'discount_price'
    ]


# Using ItemVariation as inline model field
class ItemVariationAdmin(admin.ModelAdmin):
    list_display = [
        'variation',
        'value',
        'attachment'
    ]

    # add a search field and search by values
    search_fields = ['value']
    # filter by variation
    list_filter = ['variation']


# specify the inline admin model
class ItemVariationInlineAdmin(admin.TabularInline):
    model = ItemVariation
    extra = 1  # extra 1 row in the font size


# create variation Admin
class VariationAdmin(admin.ModelAdmin):
    # add a list display for Variation from the Variation Model class
    list_display = [
        'item',
        'name'
    ]

    # add a search field and search by item
    search_fields = ['item']
    # filter by name
    list_filter = ['name']

    # add Inline admin
    inlines = [ItemVariationInlineAdmin]


# Registration or linking of all the classes in the models.py file.
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order),
admin.site.register(Variation, VariationAdmin)  # register using VariationAdmin,
admin.site.register(ItemVariation, ItemVariationAdmin)  # register using ItemVariationAdmin
