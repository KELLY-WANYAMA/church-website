from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Sermon, Event


def home(request):
    recent_sermons = Sermon.objects.order_by('-date')[:3]
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    
    context = {
        'recent_sermons': recent_sermons,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'ack/home.html', context)

def about(request):
    return render(request, 'ack/about.html')

def sermons(request):
    return render(request, 'ack/sermons.html')

def contacts(request):
    return render(request, 'ack/contacts.html')

def bk(request):
    return render(request, 'ack/bk.html')

def events(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    context = {
        'upcoming_events': upcoming_events,
        'events': upcoming_events,
    }
    return render(request, 'ack/events.html', context)

def gallery(request):
    return render(request, 'ack/gallery.html')

def giving(request):
    return render(request, 'ack/giving.html')

def full_calendar(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'ack/calendar.html', {
        'events': events
    })

def ministries(request):
    return render(request, 'ack/ministries.html')

def youth(request):
    return render(request, 'ack/youth.html')

def sundayschool(request):
    return render(request, 'ack/sundayschool.html')

def mu(request):
    return render(request, 'ack/mu.html')

def kama(request):
    return render(request, 'ack/kama.html')




