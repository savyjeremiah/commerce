from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:food>/', views.category_view, name='category_view'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('search_view/', views.search_view, name='search_view'),
    path('add_shipping_address/', views.add_shipping_address, name='add_shipping_address'),
    path('shipping_address_list/', views.shipping_address_list, name='shipping_address_list'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

