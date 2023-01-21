from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('login/', views.loginView, name='login_view'),
    path('logout/', views.logoutView, name='logout_view'),
    path('room/<str:id>/', views.room, name='room_view'),
    path('create-room/', views.createRoom, name='create_room_view'),
    path('update-room/<str:id>/', views.updateRoom, name='update_room_view'),
    path('delete-room/<str:id>/', views.deleteRoom, name='delete_room_view')
]
