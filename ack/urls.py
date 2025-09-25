from django.urls import path
from . import views
from django.http import HttpResponse
from django.templatetags.static import static




def test_static(request):
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Static Test</title>
        <link rel="stylesheet" href="{static('css/style.css')}">
        <style>
            .test {{ color: red; font-size: 20px; }}
        </style>
    </head>
    <body>
        <h1>Static File Test</h1>
        <p class="test">This should be red if inline CSS works</p>
        <p>CSS file path: {static('css/style.css')}</p>
        <p>If external CSS works, you'll see additional styles.</p>
    </body>
    </html>
    """)






urlpatterns = [
    # Main site navigation
    path('test-static/', test_static),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
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
    path('sermons/', views.sermons, name='sermons'),
    path('leaders/', views.leaders, name='leaders'),
]