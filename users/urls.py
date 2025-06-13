from django.urls import path
from . import views
from .views import login, logout, signup

urlpatterns = [
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout'),
    path('signup/', signup, name='signup'),
]
