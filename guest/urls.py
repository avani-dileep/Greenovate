from django.urls import path
from . import views  # Import the views from your app

app_name = 'guest'


urlpatterns = [
    path('', views.mainpage, name='main'),  # Home page at /user/
    
    
    
]
