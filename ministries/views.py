from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q
import json
from .models import *


# REST Framework imports
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Ministry, Program, InterestFormSubmission, MinistryMember, Event, MinistryGallery
from .serializers import (
    MinistryListSerializer, MinistryDetailSerializer, ProgramSerializer,
    InterestFormSubmissionSerializer, InterestFormCreateSerializer,
    MinistryMemberSerializer, MinistryEventSerializer, MinistryGallerySerializer,
    MinistryStatsSerializer, MinistryTypeStatsSerializer
)

def youth_ministry(request):
    # Fetch active weekly programs
    weekly_programs = WeeklyProgram.objects.filter(is_active=True)
    
    # Fetch upcoming youth events
    upcoming_events = YouthEvent.objects.filter(is_upcoming=True)
    
    # Fetch active youth leaders
    youth_leaders = YouthLeader.objects.filter(is_active=True)
    
    # Fetch active gallery images
    gallery_images = YouthGallery.objects.filter(is_active=True)[:8]  # Limit to 8 images
    
    # Fetch active parent resources
    parent_resources = VisitorResource.objects.filter(is_active=True)
    
    context = {
        'weekly_programs': weekly_programs,
        'upcoming_events': upcoming_events,
        'youth_leaders': youth_leaders,
        'gallery_images': gallery_images,
        'parent_resources': parent_resources,
    }
    
    return render(request, 'youth_ministry.html', context)


@require_POST  # Add this decorator to ensure only POST requests are accepted

def mothers_union_page(request):
    activities = MothersUnionActivity.objects.filter(is_active=True)
    leaders = MothersUnionLeader.objects.filter(is_active=True)
    events = MothersUnionEvent.objects.filter(is_active=True).order_by('date')[:6]  # Limit to 6 events
    
    context = {
        'activities': activities,
        'leaders': leaders,
        'events': events,
    }
    return render(request, 'mothers_union.html', context)


@csrf_exempt
def submit_membership_interest(request):
    if request.method == 'POST':
        try:
            print("Received membership interest request")  # Debug log
            
            # Get form data - handle both FormData and JSON
            if request.content_type == 'application/json':
                # If sending as JSON
                data = json.loads(request.body)
                full_name = data.get('full_name')
                email = data.get('email')
                phone = data.get('phone')
                message = data.get('message')
            else:
                # If sending as FormData (traditional form submission)
                full_name = request.POST.get('full_name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                message = request.POST.get('message')
            
            print(f"Form data: {full_name}, {email}, {phone}")  # Debug log
            
            # Validate required fields
            if not all([full_name, email, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields.'
                })
            
            # Save to database
            membership = MothersUnionMembership.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                message=message
            )
            
            print(f"Membership saved with ID: {membership.id}")  # Debug log
            
            # Send WhatsApp message to secretary
            send_whatsapp_notification(membership)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your interest! We will contact you soon.'
            })
            
        except Exception as e:
            print(f"Error in submit_membership_interest: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def send_whatsapp_notification(membership):
    try:
        secretary_phone = getattr(settings, 'MOTHERS_UNION_SECRETARY_PHONE', '')
        
        if secretary_phone and hasattr(settings, 'TWILIO_ACCOUNT_SID'):
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=f"""
                    New Mother's Union Membership Interest!
                    Name: {membership.full_name}
                    Email: {membership.email}
                    Phone: {membership.phone or 'Not provided'}
                    Message: {membership.message}
                """,
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f'whatsapp:{secretary_phone}'
            )
            print(f"WhatsApp message sent: {message.sid}")
        else:
            # Fallback to email or console log
            print(f"WhatsApp notification: New interest from {membership.full_name}")
            
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")




# Add to your views.py temporarily
def debug_membership(request):
    if request.method == 'POST':
        print("DEBUG: Received POST request")
        print("DEBUG: Headers:", dict(request.headers))
        print("DEBUG: POST data:", dict(request.POST))
        return JsonResponse({'status': 'debug', 'message': 'Request received'})
    return JsonResponse({'status': 'error', 'message': 'GET not allowed'})



def send_email_notification(membership):
    try:
        subject = "New Mother's Union Membership Interest"
        message = f"""
                New membership interest received:

                Name: {membership.full_name}
                Email: {membership.email}
                Phone: {membership.phone or 'Not provided'}
                Message: {membership.message}

                Please follow up within 48 hours.
            """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['wanyamakelvin47@gmail.com'],  # Replace with actual email
            fail_silently=False,
        )
        print("Email notification sent")
    except Exception as e:
        print(f"Error sending email: {e}")






# Traditional Django Views (UNCHANGED)
def ministries_home(request):
    ministries = Ministry.objects.filter(is_active=True)
    context = {
        'title': 'Ministries',
        'page_description': 'Explore our various church ministries',
        'ministries': ministries,
    }
    return render(request, 'ministries/ministries_home.html', context)


def youth_ministry(request):
    try:
        ministry = get_object_or_404(Ministry, ministry_type='youth', is_active=True)
        
        # Keep both - use WeeklyProgram for the template and ministry.programs for other purposes
        weekly_programs = ministry.programs.all()  # Your original Program model
        weekly_template_programs = WeeklyProgram.objects.filter(is_active=True).order_by('order', 'name')  # For template
        
        # Use YouthEvent for upcoming events
        from datetime import datetime
        upcoming_events = YouthEvent.objects.filter(
            event_date__gte=datetime.now()
        ).order_by('event_date')[:5]
        
        # Get youth leaders
        youth_leaders = YouthLeader.objects.filter(is_active=True)
        
        # Get gallery images
        gallery_images = YouthGallery.objects.filter(is_active=True)[:8]
        
        # Get parent resources
        parent_resources = VisitorResource.objects.filter(is_active=True)
        
        context = {
            'title': 'Youth Ministry',
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'weekly_programs': weekly_template_programs,  # Use WeeklyProgram for template compatibility
            'ministry_programs': weekly_programs,  # Keep original programs for other uses
            'upcoming_events': upcoming_events,
            'youth_leaders': youth_leaders,
            'gallery_images': gallery_images,
            'parent_resources': parent_resources,
        }
    except Ministry.DoesNotExist:
        context = {
            'title': 'Youth Ministry',
            'page_description': 'Our vibrant youth community for teens ages 12-18',
            'ministry_name': 'IGNITE Youth',
            'weekly_programs': [],
            'ministry_programs': [],
            'upcoming_events': [],
            'youth_leaders': [],
            'gallery_images': [],
            'parent_resources': [],
        }
    
    return render(request, 'ministries/youth.html', context)


def children_ministry(request):
    try:
        ministry = get_object_or_404(Ministry, ministry_type='children', is_active=True)
        programs = ministry.programs.all()
        
        context = {
            'title': 'Children Ministry',
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
        }
    except Ministry.DoesNotExist:
        context = {
            'title': 'Children Ministry',
            'page_description': 'Nurturing young hearts and minds in faith',
            'ministry_name': 'Sunday School',
            'programs': []
        }
    return render(request, 'ministries/sundayschool.html', context)

def women_ministry(request):
    try:
        ministry = get_object_or_404(Ministry, ministry_type='women', is_active=True)
        programs = ministry.programs.all()
        
        context = {
            'title': "Mother's Union",
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
        }
    except Ministry.DoesNotExist:
        context = {
            'title': "Mother's Union",
            'page_description': "Women's ministry focused on family values and community service",
            'ministry_name': "Mother's Union ACK",
            'programs': [
                {
                    'name': 'Weekly Prayer Meeting',
                    'time': 'Wednesdays, 2:00 PM',
                    'location': 'Church Chapel',
                    'description': 'Intercessory prayer for families'
                },
                {
                    'name': 'Family Support',
                    'time': 'Monthly',
                    'location': 'Various Locations',
                    'description': 'Community outreach and counseling'
                }
            ]
        }
    return render(request, 'ministries/mu.html', context)

def men_ministry(request):
    try:
        ministry = get_object_or_404(Ministry, ministry_type='men', is_active=True)
        programs = ministry.programs.all()
        
        context = {
            'title': 'Men Ministry',
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
        }
    except Ministry.DoesNotExist:
        context = {
            'title': 'Men Ministry',
            'page_description': 'Kenya Anglican Men Association focused on spiritual growth and service',
            'ministry_name': 'KAMA',
            'programs': []
        }
    return render(request, 'ministries/kama.html', context)

def choir_ministry(request):
    try:
        ministry = get_object_or_404(Ministry, ministry_type='choir', is_active=True)
        programs = ministry.programs.all()
        
        context = {
            'title': "Choir & Worship Ministry",
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
        }
    except Ministry.DoesNotExist:
        context = {
            'title': "Choir & Worship Ministry",
            'page_description': "Music ministry leading worship through choir and contemporary praise",
            'ministry_name': "ACK Music Ministry",
            'programs': []
        }
    return render(request, 'ministries/choir_worship.html', context)

def choir_worship(request):
    return choir_ministry(request)

def ministry_detail(request, ministry_type):
    """Generic ministry detail view that handles any ministry type"""
    try:
        ministry = get_object_or_404(Ministry, ministry_type=ministry_type, is_active=True)
        programs = ministry.programs.all()
        
        context = {
            'title': ministry.name,
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
        }
        
        template_name = f'ministries/{ministry_type}.html'
        return render(request, template_name, context)
        
    except Ministry.DoesNotExist:
        return render(request, 'ministries/not_found.html', {'ministry_type': ministry_type})
    

def events(request):
    # Get filter from URL parameters
    event_filter = request.GET.get('filter', 'all')
    
    # Get all events ordered by date (newest first)
    all_events = Event.objects.all().order_by('-date')
    
    # Apply filter if not 'all'
    if event_filter and event_filter != 'all':
        all_events = all_events.filter(event_type=event_filter)
    
    # Separate upcoming and past events
    today = timezone.now().date()
    upcoming_events = all_events.filter(date__gte=today)
    past_events = all_events.filter(date__lt=today)
    
    context = {
        'all_events': all_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'current_filter': event_filter,
        'title': 'Church Events & Calendar',
    }
    
    return render(request, 'events.html', context)


# NEW API VIEWS

class MinistryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for ministries"""
    queryset = Ministry.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MinistryListSerializer
        return MinistryDetailSerializer
    
    @action(detail=True, methods=['get'])
    def programs(self, request, pk=None):
        ministry = self.get_object()
        programs = ministry.programs.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        ministry = self.get_object()
        members = ministry.members.filter(is_active=True)
        serializer = MinistryMemberSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        ministry = self.get_object()
        events = ministry.events.filter(date__gte=timezone.now().date())
        serializer = MinistryEventSerializer(events, many=True)
        return Response(serializer.data)


class ProgramListAPIView(generics.ListAPIView):
    """API endpoint for all programs"""
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class MinistryProgramsAPIView(generics.ListAPIView):
    """API endpoint for programs by ministry"""
    serializer_class = ProgramSerializer
    
    def get_queryset(self):
        ministry_type = self.kwargs['ministry_type']
        return Program.objects.filter(ministry__ministry_type=ministry_type)


class InterestFormSubmissionViewSet(viewsets.ModelViewSet):
    """API endpoint for interest form submissions"""
    queryset = InterestFormSubmission.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InterestFormCreateSerializer
        return InterestFormSubmissionSerializer
    
    @action(detail=True, methods=['post'])
    def mark_contacted(self, request, pk=None):
        submission = self.get_object()
        notes = request.data.get('notes', '')
        submission.mark_contacted(notes)
        return Response({'status': 'marked as contacted'})
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = self.get_queryset().filter(is_contacted=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


# Function-based API views
@api_view(['GET'])
def ministry_stats(request):
    """API endpoint for ministry statistics"""
    total_ministries = Ministry.objects.filter(is_active=True).count()
    active_members = MinistryMember.objects.filter(is_active=True).count()
    total_programs = Program.objects.count()
    pending_interest_forms = InterestFormSubmission.objects.filter(is_contacted=False).count()
    recent_submissions = InterestFormSubmission.objects.filter(is_contacted=False)[:5]
    
    stats = {
        'total_ministries': total_ministries,
        'active_members': active_members,
        'total_programs': total_programs,
        'pending_interest_forms': pending_interest_forms,
        'recent_submissions': InterestFormSubmissionSerializer(recent_submissions, many=True).data
    }
    
    serializer = MinistryStatsSerializer(stats)
    return Response(serializer.data)


@api_view(['GET'])
def ministry_type_stats(request):
    """API endpoint for statistics by ministry type"""
    stats = []
    for ministry_type, display_name in Ministry.MINISTRY_TYPES:
        ministries = Ministry.objects.filter(ministry_type=ministry_type, is_active=True)
        program_count = Program.objects.filter(ministry__ministry_type=ministry_type).count()
        
        stats.append({
            'ministry_type': ministry_type,
            'display_name': display_name,
            'count': ministries.count(),
            'active_programs': program_count
        })
    
    serializer = MinistryTypeStatsSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def submit_interest_form(request):
    """API endpoint for submitting interest forms"""
    serializer = InterestFormCreateSerializer(data=request.data)
    
    if serializer.is_valid():
        submission = serializer.save()
        
        # Send email notification
        try:
            send_interest_email_notification(submission)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Email sending failed: {e}")
        
        return Response(
            {'status': 'success', 'message': 'Thank you for your interest!'},
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_interest_email_notification(submission):
    """Send email notification for new interest form submission"""
    subject = f"New {submission.get_ministry_type_display()} Interest - {submission.full_name}"
    message = f"""
    New Interest Form Submission:
    
    Ministry: {submission.get_ministry_type_display()}
    Name: {submission.full_name}
    Email: {submission.email}
    Phone: {submission.phone_number}
    
    Message:
    {submission.message}
    
    Submitted on: {submission.submission_date.strftime('%Y-%m-%d %H:%M:%S')}
    
    Please follow up with this interested person.
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['ministries@yourchurch.org'],  # Replace with actual email
        fail_silently=True,
    )


# Updated existing interest form views to use serializers
@csrf_exempt
@require_POST
def mothers_union_interest(request):
    return handle_interest_form(request, 'mothers_union')

@csrf_exempt
@require_POST
def kama_interest(request):
    return handle_interest_form(request, 'kama')

@csrf_exempt
@require_POST
def youth_interest(request):
    return handle_interest_form(request, 'youth')

@csrf_exempt
@require_POST
def choir_interest(request):
    return handle_interest_form(request, 'choir')

def handle_interest_form(request, ministry_type):
    """Unified handler for interest forms using serializer"""
    try:
        data = json.loads(request.body)
        data['ministry_type'] = ministry_type
        
        serializer = InterestFormCreateSerializer(data=data)
        
        if serializer.is_valid():
            submission = serializer.save()
            
            # Send email notification
            try:
                send_interest_email_notification(submission)
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Thank you for your interest! We will contact you soon.'
            })
        else:
            return JsonResponse({
                'status': 'error', 
                'message': 'Please check your form data.',
                'errors': serializer.errors
            })
            
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'})