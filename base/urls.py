from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('rooms/', views.room, name='room_view')
]
