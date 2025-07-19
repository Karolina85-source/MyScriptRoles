from django.urls import path
from . import views
from .views import logout_view



urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('add/', views.add_script, name='add_script'),
    path('delete/<int:script_id>/', views.delete_script, name='delete_script'),
    path('view/<int:script_id>/', views.view_script, name='view_script'),
    path('choose/<int:script_id>/', views.choose_roles, name='choose_roles'),
    path('logout/', logout_view, name='logout'),
    path('login/', views.custom_login, name='login'),

]