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

from .serializers import (
    MinistryListSerializer, MinistryDetailSerializer, ProgramSerializer,
    InterestFormSubmissionSerializer, InterestFormCreateSerializer,
    MinistryMemberSerializer, MinistryEventSerializer,
    MinistryStatsSerializer, MinistryTypeStatsSerializer
)

# ============================================================================
# TRADITIONAL DJANGO VIEWS - PAGE RENDERING
# ============================================================================

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
    """
    Sunday School - Children Ministry page
    """
    # DEBUG: Check if URL resolves
    from django.urls import reverse
    try:
        url = reverse('submit_sunday_school_registration')
        print(f"DEBUG: URL found: {url}")
    except Exception as e:
        print(f"DEBUG: URL error: {e}")
    
    try:
        # Get Sunday School schedules with their items
        schedules = SundaySchoolSchedule.objects.filter(is_active=True).prefetch_related('items')
        
        # Get Sunday School teachers
        teachers = SundaySchoolTeacher.objects.filter(is_active=True)
        
        # Get Sunday School information (Why Join Us, Requirements)
        why_join_info = SundaySchoolInfo.objects.filter(info_type='why_join', is_active=True).first()
        requirements_info = SundaySchoolInfo.objects.filter(info_type='requirements', is_active=True).first()
        
        context = {
            'schedules': schedules,
            'teachers': teachers,
            'why_join_info': why_join_info,
            'requirements_info': requirements_info,
            'title': 'Sunday School - Children Ministry',
        }
        
        return render(request, 'ministries/sundayschool.html', context)
        
    except Exception as e:
        print(f"Error loading Sunday School data: {e}")
        # Fallback context
        context = {
            'schedules': [],
            'teachers': [],
            'why_join_info': None,
            'requirements_info': None,
            'title': 'Sunday School - Children Ministry',
        }
        return render(request, 'ministries/sundayschool.html', context)

def choir_ministry(request):
    print("🎵 DEBUG: choir_ministry view is DEFINITELY being called!")
    print("🎵 DEBUG: Request path:", request.path)
    
    try:
        ministry = get_object_or_404(Ministry, ministry_type='choir', is_active=True)
        programs = ministry.programs.all()
        
        # Get music ministry teams
        music_teams = MusicMinistryTeam.objects.filter(is_active=True).order_by('order', 'name')
        
        print(f"🎵 DEBUG: Found {music_teams.count()} music teams")
        for team in music_teams:
            print(f"🎵 DEBUG: Team - {team.name}")
        
        context = {
            'title': "Choir & Worship Ministry",
            'page_description': ministry.description,
            'ministry_name': ministry.name,
            'ministry': ministry,
            'programs': programs,
            'music_teams': music_teams,
        }
    except Ministry.DoesNotExist:
        print("🎵 DEBUG: Ministry not found, using fallback")
        music_teams = MusicMinistryTeam.objects.filter(is_active=True).order_by('order', 'name')
        
        context = {
            'title': "Choir & Worship Ministry",
            'page_description': "Music ministry leading worship through choir and contemporary praise",
            'ministry_name': "ACK Music Ministry",
            'programs': [],
            'music_teams': music_teams,
        }
    
    print("🎵 DEBUG: Rendering template with context")
    return render(request, 'ministries/choir_worship.html', context)

def choir_worship(request):
    print("🎵 DEBUG: choir_worship view is DEFINITELY being called!")
    print("🎵 DEBUG: Request path:", request.path)
    return choir_ministry(request)

def mothers_union_page(request):
    # Fetch all active Mother's Union data
    activities = MothersUnionActivity.objects.filter(is_active=True).order_by('order')
    leaders = MothersUnionLeader.objects.filter(is_active=True).order_by('order')
    
    # Get upcoming events (future dates only)
    from datetime import date
    events = MothersUnionEvent.objects.filter(
        is_active=True, 
        date__gte=date.today()
    ).order_by('date')[:6]  # Limit to 6 upcoming events
    
    # Also get the ministry object if needed
    try:
        ministry = Ministry.objects.get(ministry_type='women', is_active=True)
    except Ministry.DoesNotExist:
        ministry = None
    
    context = {
        'activities': activities,
        'leaders': leaders,
        'events': events,
        'ministry': ministry,
        'title': "Mother's Union",
    }
    return render(request, 'ministries/mu.html', context)

def men_ministry(request):
    """
    KAMA - Men Ministry page
    """
    try:
        # Get KAMA motto (only active one)
        motto = KamaMotto.objects.filter(is_active=True).first()
        
        # Get KAMA activities
        activities = KamaActivity.objects.filter(is_active=True).order_by('order')
        
        # Get KAMA leaders
        leaders = KamaLeader.objects.filter(is_active=True).order_by('order')
        
        # Also get the ministry object if needed
        try:
            ministry = Ministry.objects.get(ministry_type='men', is_active=True)
        except Ministry.DoesNotExist:
            ministry = None
        
        context = {
            'motto': motto,
            'activities': activities,
            'leaders': leaders,
            'ministry': ministry,
            'title': 'KAMA - Men Ministry',
        }
        
        # Make sure the template path is correct
        return render(request, 'ministries/kama.html', context)
        
    except Exception as e:
        print(f"Error loading KAMA data: {e}")
        # Fallback context
        context = {
            'motto': None,
            'activities': [],
            'leaders': [],
            'title': 'KAMA - Men Ministry',
        }
        return render(request, 'ministries/kama.html', context)

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

def ministry_detail(request, ministry_type):
    print(f"🎵 DEBUG: ministry_detail called with ministry_type: '{ministry_type}'")
    print(f"🎵 DEBUG: Request path: {request.path}")
    
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

# ============================================================================
# FORM SUBMISSION HANDLERS
# ============================================================================

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

@require_POST
@csrf_exempt
def submit_sunday_school_registration(request):
    """
    Handle Sunday School registration form submissions
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['child_name', 'child_age', 'age_group', 'parent_name', 'phone']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            })

        # Validate age
        try:
            child_age = int(data.get('child_age'))
            if child_age < 3 or child_age > 12:
                return JsonResponse({
                    'success': False,
                    'message': 'Child age must be between 3 and 12 years.'
                })
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'message': 'Invalid age format.'
            })

        # Create new registration
        registration = SundaySchoolRegistration(
            child_name=data.get('child_name'),
            child_age=child_age,
            age_group=data.get('age_group'),
            parent_name=data.get('parent_name'),
            phone=data.get('phone'),
            email=data.get('email'),
            special_notes=data.get('special_notes')
        )
        registration.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for registering your child! We will contact you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}. Please try again later.'
        }, status=500)

@csrf_exempt
@require_POST
def submit_music_ministry_registration(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['full_name', 'phone', 'team', 'experience', 'instrument', 'message']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            })

        # Create registration
        registration = MusicMinistryRegistration(
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            email=data.get('email', ''),
            team=data.get('team'),
            experience=data.get('experience'),
            instrument=data.get('instrument'),
            message=data.get('message')
        )
        registration.save()
        
        # Send WhatsApp notifications based on team selection
        send_music_ministry_whatsapp_notification(registration)
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your registration! We will contact you soon.'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

# ============================================================================
# API VIEWSETS AND CLASS-BASED VIEWS
# ============================================================================

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

# ============================================================================
# API FUNCTION-BASED VIEWS
# ============================================================================

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

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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

def send_music_ministry_whatsapp_notification(registration):
    """Send WhatsApp notifications to relevant team leaders"""
    try:
        # Get team leaders based on registration
        if registration.team == 'choir':
            teams = MusicMinistryTeam.objects.filter(team_type='choir', is_active=True)
        elif registration.team == 'praise':
            teams = MusicMinistryTeam.objects.filter(team_type='praise', is_active=True)
        else:  # both
            teams = MusicMinistryTeam.objects.filter(is_active=True)
        
        for team in teams:
            if team.leader_phone:
                send_whatsapp_to_leader(registration, team)
                
    except Exception as e:
        print(f"Error sending WhatsApp notifications: {e}")

def send_whatsapp_to_leader(registration, team):
    """Send individual WhatsApp message to team leader"""
    try:
        if hasattr(settings, 'TWILIO_ACCOUNT_SID') and team.leader_phone:
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message_body = f"""
🎵 New Music Ministry Registration!

Team: {registration.get_team_display()}
Name: {registration.full_name}
Phone: {registration.phone}
Email: {registration.email or 'Not provided'}

Experience: {registration.get_experience_display()}
Instrument: {registration.get_instrument_display()}

Message:
{registration.message}

Please follow up within 48 hours.
            """
            
            message = client.messages.create(
                body=message_body.strip(),
                from_=settings.TWILIO_WHATSAPP_NUMBER,
                to=f'whatsapp:{team.leader_phone}'
            )
            print(f"WhatsApp sent to {team.leader_name}: {message.sid}")
        else:
            print(f"WhatsApp notification for {team.leader_name}: New registration from {registration.full_name}")
            
    except Exception as e:
        print(f"Error sending WhatsApp to {team.leader_name}: {e}")

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