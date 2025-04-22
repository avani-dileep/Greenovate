from django.urls import path
from . import views  # Import the views from your app
from django.contrib.auth import views as auth_views

app_name = 'recycler'  

urlpatterns = [
    
    path('', views.recycler_index, name='recycler_index'),
    path("recycler_signin/", views.recycler_signin, name="recycler_signin"),
    path("recycler_logout/", views.recycler_logout, name="recycler_logout"), 
    path("recycler_profile/", views.recycler_profile, name="recycler_profile"), 
    path("recycler_request_garbage/", views.recycler_request_garbage, name="recycler_request_garbage"),
    path("view_requests/", views.view_requests, name="view_requests"),
    path("add_recycled_product/", views.add_recycled_product, name="add_recycled_product"),
    path("view_products/", views.view_products, name="view_products"),
    path("edit_product/<int:product_id>/", views.edit_product, name="edit_product"),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('order_details/', views.order_details, name='order_details'),  # View orders
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),  # Update status
    path('completed_orders/', views.completed_orders, name='completed_orders'),
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('daily_orders/', views.daily_orders, name='daily_orders'),
    path("submit_complaint/", views.submit_complaint, name="submit_complaint"),
    path("view_complaints/", views.view_complaints, name="view_complaints"),
    path("user_feedback/", views.user_feedback, name="user_feedback"),
    path('ordered_users/', views.ordered_users, name='ordered_users'),
]

    
    



