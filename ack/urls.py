from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # Traditional URLs (existing)
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('sermons/', views.sermons, name='sermons'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('giving/', views.giving, name='giving'),
    path('calendar/', views.full_calendar, name='full_calendar'),
    path('ministries/', views.ministries, name='ministries'),
    path('youth/', views.youth, name='youth'),
    path('sundayschool/', views.sundayschool, name='sundayschool'),
    path('mu/', views.mu, name='mu'),
    path('kama/', views.kama, name='kama'),
    path('leaders/', views.leaders, name='leaders'),
    
    # NEW API URLs
    path('api/', api_home, name='api-home'),
    path('api/sermons/<int:pk>/', SermonDetailAPIView.as_view(), name='api-sermon-detail'),
    path('api/sermons/create/', SermonCreateAPIView.as_view(), name='api-sermon-create'),
    path('api/events/', EventListAPIView.as_view(), name='api-events'),
    path('api/events/upcoming/', UpcomingEventsAPIView.as_view(), name='api-events-upcoming'),
    path('api/events/<int:pk>/', EventDetailAPIView.as_view(), name='api-event-detail'),
    path('api/events/create/', EventCreateAPIView.as_view(), name='api-event-create'),
    path('api/event-types/', event_types_api, name='api-event-types'),
]