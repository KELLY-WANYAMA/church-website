from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


# Traditional Django Views - Updated for better integration
def home(request):
    recent_sermons = SermonEvent.objects.all()[:3]  # Uses model ordering
    upcoming_events = Event.objects.filter(date__gte=timezone.now())[:3]  # Uses model ordering
    
    context = {
        'recent_sermons': recent_sermons,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'ack/home.html', context)

def about(request):
    leaders = Leader.objects.filter(is_active=True).order_by('order', 'position')
    
    context = {
        'leaders': leaders,
    }
    return render(request, 'ack/about.html', context)


def sermons(request):
    """Sermons page with services and past events"""
    # Get active church services
    services = ChurchService.objects.filter(is_active=True).order_by('order', 'service_type')
    
    # Get past sermon events (events before today)
    from datetime import date
    past_events = SermonEvent.objects.filter(
        is_active=True, 
        event_date__lt=date.today()
    ).order_by('-event_date')[:6]  # Limit to 6 most recent events
    
    context = {
        'title': 'Sermons & Services',
        'page_description': 'Watch our latest sermons and explore our church services',
        'services': services,
        'past_events': past_events,
    }
    
    return render(request, 'ack/sermons.html', context)



def contacts(request):
    return render(request, 'ack/contacts.html')


def events(request):
    # Get filter parameter from request
    event_type = request.GET.get('type', 'all')
    
    # Debug: Print the filter being received
    print(f"DEBUG: Event type filter requested: '{event_type}'")
    
    # Get ALL events ordered by date
    all_events = Event.objects.all().order_by('-date')
    
    # Filter events by type if specified
    if event_type != 'all':
        # Use exact match for event_type (case-sensitive)
        all_events = all_events.filter(event_type=event_type)
        print(f"DEBUG: After filtering by '{event_type}', found {all_events.count()} events")
    
    # Separate upcoming and past events - handle DateTimeField properly
    now = timezone.now()
    upcoming_events = [event for event in all_events if event.date >= now]
    past_events = [event for event in all_events if event.date < now]
    
    # Debug: Print final counts
    print(f"DEBUG: Final counts - All: {len(all_events)}, Upcoming: {len(upcoming_events)}, Past: {len(past_events)}")
    
    context = {
        'all_events': all_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'current_filter': event_type,
    }
    return render(request, 'ack/events.html', context)

def gallery(request):
    # Get all gallery items ordered by date
    gallery_items = Gallery.objects.all().order_by('-event_date', '-created_at')
    
    # Get filter from request
    category_filter = request.GET.get('category', 'all')
    
    print(f"DEBUG: Category filter requested: '{category_filter}'")
    
    # Filter by category if specified
    if category_filter != 'all':
        gallery_items = gallery_items.filter(category=category_filter)
        print(f"DEBUG: After filtering, found {gallery_items.count()} items")
    
    # Get featured items
    featured_items = Gallery.objects.filter(is_featured=True)[:5]
    
    # Get UNIQUE categories - use distinct() to avoid duplicates
    unique_categories = Gallery.objects.values_list('category', flat=True).distinct().order_by('category')
    
    # Debug: Print what we're getting
    print(f"DEBUG: Unique categories: {list(unique_categories)}")
    
    context = {
        'gallery_items': gallery_items,
        'featured_items': featured_items,
        'current_category': category_filter,
        'unique_categories': unique_categories,
    }
    return render(request, 'ack/gallery.html', context)


def giving(request):
    return render(request, 'ack/giving.html')

def full_calendar(request):
    events = Event.objects.all()  # Uses model ordering
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

def leaders(request):
    return render(request, 'ack/leaders.html')


# API Views - Updated for better integration

class SermonDetailAPIView(generics.RetrieveAPIView):
    """API endpoint for single sermon details"""
    queryset = SermonEvent.objects.all()
    serializer_class = SermonSerializer

# Event API Views
class EventListAPIView(generics.ListAPIView):
    """API endpoint for listing events"""
    queryset = Event.objects.all()  # Uses model ordering
    serializer_class = EventListSerializer

class UpcomingEventsAPIView(generics.ListAPIView):
    """API endpoint for upcoming events"""
    queryset = Event.objects.filter(date__gte=timezone.now())  # Uses model ordering
    serializer_class = EventListSerializer

class EventDetailAPIView(generics.RetrieveAPIView):
    """API endpoint for single event details"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Function-based API views
@api_view(['GET'])
def api_home(request):
    """API homepage with summary data"""
    recent_sermons = SermonEvent.objects.all()[:3]
    upcoming_events = Event.objects.filter(date__gte=timezone.now())[:5]
    
    event_serializer = EventListSerializer(upcoming_events, many=True)
    
    return Response({
        'upcoming_events': event_serializer.data,
        'total_sermons': SermonEvent.objects.count(),
        'total_events': Event.objects.count(),
    })

@api_view(['GET'])
def event_types_api(request):
    """API endpoint to get event type choices"""
    event_types = [
        {'value': value, 'display': display}
        for value, display in Event.EVENT_TYPES
    ]
    return Response(event_types)

# Admin API views (for creating/updating content)
class SermonCreateAPIView(generics.CreateAPIView):
    """API endpoint for creating sermons (admin use)"""
    queryset = SermonEvent.objects.all()
    serializer_class = SermonSerializer

class EventCreateAPIView(generics.CreateAPIView):
    """API endpoint for creating events (admin use)"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Update API views
class SermonUpdateAPIView(generics.UpdateAPIView):
    """API endpoint for updating sermons (admin use)"""
    queryset = SermonEvent.objects.all()
    serializer_class = SermonSerializer

class EventUpdateAPIView(generics.UpdateAPIView):
    """API endpoint for updating events (admin use)"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer