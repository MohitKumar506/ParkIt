from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('display',views.display,name='display'),
    path('provider',views.provider,name='provider'),
    path('need',views.need,name='need'),
    path('pdashboard',views.pdashboard,name='pdashboard'),
    path('delLocation/<int:pk>',views.delLocation,name='delLocation'),
    path('show',views.show,name='show'),
    path('myBookings/<int:id>', views.myBookings, name='myBookings'),
    path('book',views.book,name='book'),
    path('find/<int:id>', views.find, name='find'),
    path('tripOver/<int:id>', views.tripOver, name='tripOver'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
