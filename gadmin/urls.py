from django.urls import path
from . import views  # Import the views from your app

app_name = 'gadmin'


urlpatterns = [
    path('gadminhome', views.gadminhome, name='gadminhome'),  # Home page at /user/
    path("admin_signup/", views.admin_signup, name="admin_signup"),
    path("", views.admin_signin, name="admin_signin"),
    path('add_driver/', views.add_driver, name='add_driver'),
    path('view_driver/', views.view_driver, name='view_driver'),
    path('edit_driver/<str:driver_id>/', views.edit_driver, name='edit_driver'),
    path('delete_driver/<str:driver_id>/', views.delete_driver, name='delete_driver'),
    path('add_recycler/', views.add_recycler, name='add_recycler'),
    path('view_recycler/', views.view_recycler, name='view_recycler'),
    path("edit_recycler/<str:recycler_id>/", views.edit_recycler, name="edit_recycler"),
    path("delete_recycler/<str:recycler_id>/", views.delete_recycler, name="delete_recycler"),
    path("manage_garbage/", views.manage_garbage, name="manage_garbage"),
    path('assign_driver/<int:schedule_id>/', views.assign_driver, name='assign_driver'),
    path('assigned_drivers_list/', views.assigned_drivers_list, name='assigned_drivers_list'),
    path("manage_recycler_requests/", views.manage_recycler_requests, name="manage_recycler_requests"),
    path("update_request_status/<int:request_id>/", views.update_request_status, name="update_request_status"),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path("view_residents_complaint/", views.view_residents_complaint, name="view_residents_complaint"),
    path("view_collector_complaint/", views.view_collector_complaint, name="view_collector_complaint"),
    path("view_recycler_complaints/", views.view_recycler_complaints, name="view_recycler_complaints"),
    path('daily_report/', views.daily_report, name='daily_report'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path("view_recycledproducts/", views.view_recycledproducts, name="view_recycledproducts"),
    
]
