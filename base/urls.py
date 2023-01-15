from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('room/<str:id>/', views.room, name='room_view'),
    path('create-room/', views.createRoom, name='create_room_view'),
    path('update-room/<str:id>/', views.updateRoom, name='update_room_view')
]
