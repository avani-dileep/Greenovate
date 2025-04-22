from django.urls import path
from . import views  # Import the views from your app

app_name = 'customer'


urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Home page at /user/
    path('signin/', views.signin, name='signin'),  # Product page at /user/product/
    path('signup/', views.signup, name='signup'),
    path('clogout/', views.clogout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('addgarbage/', views.addgarbage, name='addgarbage'),
    path('viewgarbage/', views.viewgarbage, name='viewgarbage'),
    path('editgarbage/<int:schedule_id>/', views.editgarbage, name='editgarbage'),
    path('deletegarbage/<int:schedule_id>/', views.deletegarbage, name='deletegarbage'),
    path('addcomplaint/', views.addcomplaint, name='addcomplaint'),
    path('viewcomplaint/', views.viewcomplaint, name='viewcomplaint'),
    
    
]
