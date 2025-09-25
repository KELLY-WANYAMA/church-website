# ministries/views.py
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

def ministries_home(request):
    context = {
        'title': 'Ministries',
        'page_description': 'Explore our various church ministries',
    }
    return render(request, 'ministries/ministries_home.html', context)

def youth_ministry(request):
    context = {
        'title': 'Youth Ministry',
        'page_description': 'Our vibrant youth community for teens ages 12-18',
        'ministry_name': 'IGNITE Youth',
        'programs': [
            {
                'name': 'Sunday School',
                'time': 'Sundays, 9:30-10:30am',
                'location': 'Youth Room',
                'description': 'Bible study and discussion groups'
            },
            {
                'name': 'Youth Night',
                'time': 'Wednesdays, 7-9pm',
                'location': 'Main Hall',
                'description': 'Worship, games, and relevant messages'
            }
        ]
    }
    return render(request, 'ministries/youth.html', context)

def children_ministry(request):
    context = {'title': 'Children Ministry'}
    return render(request, 'ministries/sundayschool.html', context)

def women_ministry(request):
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
    context = {'title': 'Men Ministry'}
    return render(request, 'ministries/kama.html', context)

@csrf_exempt
@require_POST
def mothers_union_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone', '')
            message = data.get('message', '')
            
            # Email content
            subject = f"New Mother's Union Interest Form - {full_name}"
            email_message = f"""
            New Interest Form Submission:
            
            Name: {full_name}
            Email: {email}
            Phone: {phone}
            
            Message:
            {message}
            
            Submitted on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Send email
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['mothersunion@yourchurch.org'],  # Replace with actual email
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Thank you for your interest! We will contact you soon.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'An error occurred. Please try again.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



def kama_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name')
            email = data.get('email')
            phone = data.get('phone', 'Not provided')
            message = data.get('message', '')
            
            # Email content
            subject = f"New KAMA Membership Interest - {full_name}"
            email_message = f"""
            New KAMA Membership Interest Form Submission:
            
            Name: {full_name}
            Email: {email}
            Phone: {phone}
            
            Message:
            {message}
            
            Submitted on: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Please follow up with this interested member.
            """
            
            # Send email to KAMA leadership
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['kama.leadership@yourchurch.org', 'pastor@yourchurch.org'],  # Add your emails here
                fail_silently=False,
            )
            
            # Optional: Send confirmation email to the user
            user_subject = "Thank you for your interest in KAMA"
            user_message = f"""
            Dear {full_name},
            
            Thank you for expressing interest in joining the Kenya Anglican Men's Association (KAMA).
            
            We have received your information and a member of our leadership team will contact you shortly.
            
            Blessings,
            KAMA Leadership Team
            ACK St Judes Huruma
            """
            
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,  # Silent fail for user email
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Thank you for your interest! Our KAMA leadership team will contact you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': 'An error occurred. Please try again or contact us directly.'
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def choir_ministry(request):
    context = {
        'title': "Choir & Worship Ministry",
        'page_description': "Music ministry leading worship through choir and contemporary praise",
        'ministry_name': "ACK Music Ministry",
    }
    return render(request, 'ministries/choir_worship.html', context)

def choir_worship(request):
    context = {
        'title': "Choir & Worship Ministry",
        'page_description': "Music ministry leading worship through choir and contemporary praise",
        'ministry_name': "ACK Music Ministry",
    }
    return render(request, 'ministries/choir_worship.html', context)

