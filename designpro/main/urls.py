from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('password_reset_question/', views.password_reset_question, name='password_reset_question'),
    path('create_application/', views.create_application, name='create_application'),
    path('application_list/', views.ApplicationListView.as_view(), name='application_list'),
    path('application/confirm_delete/<int:application_id>/', views.confirm_delete_application, name='confirm_delete_application'),
    path('application/delete/<int:application_id>/', views.delete_application, name='delete_application'),

    path('application/change_status/<int:application_id>/', views.change_status, name='change_status'),

    path('create_category/', views.create_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]