from django.urls import path
from . import views  # Import the views from your app

app_name = 'collector'


urlpatterns = [
    path('', views.collectorhome, name='collectorhome'),  # Home page at /user/
    path("driver_signin/", views.driver_signin, name="driver_signin"),
    path("driver_logout/", views.driver_logout, name="driver_logout"),
    path('view_driver_pickups/', views.view_driver_pickups, name='view_driver_pickups'),
    path('update_status', views.update_status, name='update_status'),
    path("collector_profile/", views.collector_profile, name="collector_profile"),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('view_complaint/', views.view_complaint, name='view_complaint'),
    
    
    
]
