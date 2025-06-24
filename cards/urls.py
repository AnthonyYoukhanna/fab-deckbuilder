from django.urls import path
from .views import card_list, increment_card, collection_view
from . import views

urlpatterns = [
    path('', card_list, name='card_list'),
    path('<int:card_id>/', views.card_detail, name='card_detail'),
    path('printing/<str:unique_id>/', views.card_printing_detail, name='card_printing_detail'),
    #path('increment-card/', increment_card_quantity, name='increment_card'),
]

urlpatterns += [
    path('increment-card/', views.increment_card, name='increment_card'),
    path('bulk-add/', views.bulk_add_view, name='bulk-add'),
    path('collection/', views.collection_view, name='collection'),
    ]