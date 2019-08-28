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

    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('activate/uid=<int:uid>', views.activate, name='activate'),
    
] 
