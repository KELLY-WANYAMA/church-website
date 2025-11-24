# ministries/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

# Router for ViewSets
router = DefaultRouter()
router.register(r'ministries', MinistryViewSet, basename='ministry')
router.register(r'interest-forms', InterestFormSubmissionViewSet, basename='interestform')

urlpatterns = [
    # Traditional Ministry URLs
    path('', views.ministries_home, name='ministries_home'),
    path('youth/', views.youth_ministry, name='youth_ministry'),
    path('kama/', views.men_ministry, name='men_ministry'),
    path('choir/', views.choir_ministry, name='choir_ministry'),
    path('choir_worship/', views.choir_worship, name='choir_worship'),
    path('sundayschool/', views.children_ministry, name='children_ministry'),
    path('events/', views.events, name='events'),
    
    # MOTHER'S UNION
    path('mu/', views.mothers_union_page, name='mothers_union'),
    
    # Form submissions
    path('submit_sunday_school_registration/', views.submit_sunday_school_registration, name='submit_sunday_school_registration'),
    path('submit_music_ministry_registration/', views.submit_music_ministry_registration, name='submit_music_ministry_registration'),
    path('submit-membership-interest/', views.submit_membership_interest, name='submit_membership_interest'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/stats/', ministry_stats, name='ministry_stats'),
    path('api/stats/by-type/', ministry_type_stats, name='ministry_type_stats'),
    path('api/interest/submit/', submit_interest_form, name='submit_interest_form'),
    path('api/programs/', ProgramListAPIView.as_view(), name='program_list'),
    path('api/programs/<str:ministry_type>/', MinistryProgramsAPIView.as_view(), name='ministry_programs'),
    
    # API Interest form endpoints - FIXED
    path('api/mothers-union-interest/', mothers_union_interest, name='mothers_union_interest'),
    path('api/kama-interest/', views.kama_interest, name='kama_interest'),
    path('api/youth-interest/', views.youth_interest, name='youth_interest'),
    path('api/choir-interest/', views.choir_interest, name='choir_interest'),
    
    # Keep this LAST
    path('<str:ministry_type>/', views.ministry_detail, name='ministry_detail'),
]