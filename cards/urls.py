from django.urls import path
from .views import card_list
from . import views

urlpatterns = [
    path('', card_list, name='card_list'),
    path('<int:card_id>/', views.card_detail, name='card_detail'),
    path('printing/<str:unique_id>/', views.card_printing_detail, name='card_printing_detail'),

]