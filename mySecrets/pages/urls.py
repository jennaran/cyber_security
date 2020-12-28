from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('login/', views.loginView, name='login'),
    path('add/', views.addView, name='add'),
    path('view/', views.secretView, name='secret'),
    path('logout/', views.logoutView, name='logout'),
]