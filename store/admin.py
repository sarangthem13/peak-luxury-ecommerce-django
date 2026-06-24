from django.contrib import admin
from .models import (
    Category,
    Product,
    Order,
    OrderItem,
    Review
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'user',
        'rating',
        'created_at'
    ]

    list_filter = [
        'rating',
        'created_at'
    ]


admin.site.register(Order)
admin.site.register(OrderItem)