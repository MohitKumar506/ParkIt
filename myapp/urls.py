from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('display',views.display,name='display'),
    path('provider',views.provider,name='provider'),
    path('need',views.need,name='need'),
]