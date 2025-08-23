from django.urls import path
from . import views

urlpatterns = [
    # Main site navigation
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('sermons/', views.sermons, name='senmon'),
    path('contacts/', views.contacts, name='contact'),
    path('bk/', views.bk, name='bk'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('giving/', views.giving, name='giving'),
    path('calendar/', views.full_calendar, name='full_calendar'),
    path('ministries/', views.ministries, name='ministries'),
    path('youth/', views.youth, name='youth'),
    path('sundayschool/', views.sundayschool, name='sundayschool'),
    path('mu/', views.mu, name= 'mothersunion'),
    path('kama/', views.kama, name='kama'),
    
    
]