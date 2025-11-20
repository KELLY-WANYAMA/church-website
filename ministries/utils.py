from django.core.mail import send_mail
from django.conf import settings

def send_interest_email_notification(interest_data):
    """
    Send email notification when someone expresses interest in KAMA membership
    """
    try:
        subject = f"New KAMA Membership Interest - {interest_data['full_name']}"
        message = f"""
        New KAMA Membership Interest Received:
        
        Name: {interest_data['full_name']}
        Email: {interest_data['email']}
        Phone: {interest_data.get('phone', 'Not provided')}
        
        Message:
        {interest_data['message']}
        
        Submitted at: {interest_data.get('submitted_at', 'Just now')}
        """
        
        # Send to admin email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  # Make sure ADMIN_EMAIL is in your settings
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email notification: {e}")
        return False

# Remove the undefined functions from imports
# send_whatsapp_notification and handle_interest_form are not defined