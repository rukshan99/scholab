from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('room/<str:id>/', views.room, name='room_view')
]
