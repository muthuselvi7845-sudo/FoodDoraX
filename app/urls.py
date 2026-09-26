from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('orders/<int:food_id>/',views.place_order,name='orders'),
    path('myorders/',views.my_orders,name='my_orders'),
    path('deliveryorders/',views.delivery_orders,name='delivery_orders'),
    path('delivery/advance/<int:order_id>/', views.advance_status, name='advance_status'),
    path('cart/', views.cart, name='cart'),
    path('addtocart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/online/', views.place_order_online, name='place_order_online'),
    path('payment/cod/', views.place_order_cod, name='place_order_cod'),
    path('delivery/available/', views.available_orders, name='available_orders'),
    path('delivery/accept/<int:order_id>/', views.accept_order, name='accept_order'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/retry/<int:order_id>/', views.retry_payment, name='retry_payment'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('payment/demo/confirm/<int:order_id>/', views.confirm_demo_payment, name='confirm_demo_payment'),
    path('food/<int:food_id>/', views.food_detail, name='food_detail'),
    path('food/<int:food_id>/review/', views.add_review, name='add_review'),
    path('buynow/online/<int:food_id>/', views.buy_now_online, name='buy_now_online'),
    path('buynow/cod/<int:food_id>/', views.buy_now_cod, name='buy_now_cod'),
    path('address/', views.address_list, name='address_list'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/select/<int:address_id>/', views.select_address, name='select_address'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
