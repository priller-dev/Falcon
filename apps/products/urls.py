from django.urls import path

from apps.products.views import homepage, products_list, \
    add_product, generate_fake_data, product_detail, \
    shopping_cart, add_to_shopping_cart, delete_shopping_cart_item, \
    buy_shopping_cart_items

from apps.products.views import MyProductsView, EditMyProductView, AddFavorite, DeleteMyProductView\
    , BlogView


urlpatterns = [
    path('', homepage, name='homepage'),
    path('products/', products_list,
         name='products_list'),
    path('generate_data', generate_fake_data, name='generate_data'),
    path('product_detail/<int:pk>', product_detail, name='product_detail'),
    path('blog/', BlogView.as_view())
]

for_admins = [
    path('my-products', MyProductsView.as_view(), name='my_products'),
    path(
        'edit-product/<int:pk>',
        EditMyProductView.as_view(),
        name='edit_product'
    ),
    path('add_product', add_product, name='add_product'),
    path(
        'delete-product/<int:pk>',
        DeleteMyProductView.as_view(),
        name='delete_product'
    )
]

for_users = [
    path('shopping_cart', shopping_cart, name='shopping_cart'),
    path(
        'add_to_cart/<int:pk>',
        add_to_shopping_cart,
        name='add_to_shopping_cart'),
    path('del_cart/<int:pk>', delete_shopping_cart_item,
         name='delete_shopping_cart_item'),
    path(
        'buy_shopping_cart_items',
        buy_shopping_cart_items,
        name='buy_products'
    ),
    path('add_favorite/<int:pk>', AddFavorite.as_view(), name='add_favorite')
]


urlpatterns += for_admins
urlpatterns += for_users