from django.urls import path
from . import views  # Import the views from your app
from django.contrib.auth import views as auth_views

app_name = 'user'  

urlpatterns = [
    path('', views.guest, name='guest'), 
    path('home/', views.home, name='home'),  # Home page at /user/
    
    
    path('profile/', views.profile, name='profile'),
    path('product/', views.product, name='product'),  # Product page at /user/product/
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.usignup, name='signup'),
    path('signin/', views.usignin, name='signin'),
    path('logout/', views.ulogout, name='logout'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path("checkout/", views.checkout, name="checkout"),
    path('order_success/', views.order_success, name='order_success'),
   # path("process_checkout/", views.process_checkout, name="process_checkout"),
]


