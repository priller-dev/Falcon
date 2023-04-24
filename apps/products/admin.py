from django.contrib import admin

from apps.products.models import Product, Review, Category, ProductProxy
from django.utils.safestring import mark_safe


class ProductInline(admin.StackedInline):
    model = Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name', 'price', 'short_description',
        'description', 'discount', 'quantity',
        'shipping_cost', 'specification', 'category', 'headshot_images'
    )
    list_display = ('name', 'price', 'quantity', 'category',
                    'headshot_images')

    readonly_fields = ['name', 'price', 'quantity', 'category',
                       "headshot_images"]

    def headshot_images(self, obj):
        if obj.images.first():
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.images.first().image.url,
                    width=200,
                    height=260,
                )
            )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ('user', 'body', 'product')
    list_display = ('user', 'body', 'product')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name')

    inlines = [ProductInline]


@admin.register(ProductProxy)
class ProductProxyAdmin(admin.ModelAdmin):
    fields = (
        'name', 'price', 'short_description',
        'description', 'discount', 'quantity',
        'shipping_cost', 'specification', 'category', 'is_premium'
    )
    list_display = ('name', 'price', 'quantity', 'category', 'is_premium')

    def get_queryset(self, request):
        query = super(ProductProxyAdmin, self).get_queryset(request)
        filtered_query = query.filter(is_premium=True)
        return filtered_query
