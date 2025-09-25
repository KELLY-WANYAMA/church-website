# ministries/urls.py
from django.urls import path
from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.ministries_home, name='ministries_home'),
    path('youth/', views.youth_ministry, name='youth'),
    path('sundayschool/', views.children_ministry, name='children'),
    path('mu/', views.women_ministry, name='women'),
    path('mu/interest/', views.mothers_union_interest, name='mothers_union_interest'),
    path('kama/', views.men_ministry, name='kama'),
    path('kama/interest/', views.kama_interest, name='kama_interest'),
    path('choir_worship/', views.choir_worship, name='choir_worship'),

]