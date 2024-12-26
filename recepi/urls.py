from django.urls import path
from .views import *




urlpatterns = [
    path('',recipes,name="recipes"),
    path('login_page/',login_page,name='login_page'),
    path('logout/',logout_page,name="logout_page"),
    path('register/',register,name='register'),
    path('delete_recipes/<id>/',delete_recipes,name='delete_recipes'),
    path('update_recipes/<id>/',update_recipes,name="update_recipes")
]

