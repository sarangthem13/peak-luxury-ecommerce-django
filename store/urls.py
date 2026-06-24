from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('products/', views.product_list, name='product_list'),

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'category/<slug:slug>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'search/',
        views.search_products,
        name='search_products'
    ),

    # CART

    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'increase-cart/<int:product_id>/',
        views.increase_cart,
        name='increase_cart'
    ),

    path(
        'decrease-cart/<int:product_id>/',
        views.decrease_cart,
        name='decrease_cart'
    ),

    path(
        'remove-cart/<int:product_id>/',
        views.remove_from_cart,
        name='remove_cart'
    ),

    # WISHLIST

    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    path(
        'add-to-wishlist/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'remove-from-wishlist/<int:product_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),
    # ACCOUNT

    path('login/', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),

    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile, name='profile'),

    path(
    'addresses/',
    views.addresses,
    name='addresses'
    ),
    path('orders/', views.order_history, name='order_history'),

    # OTHER PAGES

    path('checkout/', views.checkout, name='checkout'),

    path('contact/', views.contact, name='contact'),

    path('about/', views.about, name='about'),

    path('faq/', views.faq, name='faq'),
    
]