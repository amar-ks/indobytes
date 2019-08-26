from django.urls import path
from indobytes import views


app_name = 'indobytes'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('validate_email/', views.validate_email, name='validate_email'),
    path('validate_username/', views.validate_username, name='validate_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
] 
