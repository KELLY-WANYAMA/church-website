# models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, time



class Event(models.Model):
    EVENT_TYPES = [
        ('REVIVAL', 'Revival'),
        ('FELLOWSHIP', 'Fellowship'),
        ('WEDDING', 'Wedding'),
        ('PRAYER', 'Prayer'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='FELLOWSHIP')
    youtube_url = models.URLField(blank=True, null=True, help_text="Link to YouTube video of this event")
    tiktok_url = models.URLField(blank=True, null=True, help_text="Link to TikTok video of this event")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Church Homepage Events update'

    def __str__(self):
        return self.title

    def get_event_type_display(self):
        return dict(self.EVENT_TYPES).get(self.event_type, self.event_type)

    def has_video_links(self):
        return bool(self.youtube_url or self.tiktok_url)

    def is_upcoming(self):
        return self.date > timezone.now()

    def days_until_event(self):
        if self.date > timezone.now():
            delta = self.date - timezone.now()
            return delta.days
        return 0

    def formatted_date(self):
        day = self.date.day
        if 11 <= day <= 13:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return self.date.strftime(f'%d{suffix} %B %Y')

    def formatted_time(self):
        if self.time:
            return self.time.strftime('%I:%M %p')
        return self.date.strftime('%I:%M %p')

    def get_event_icon(self):
        icons = {
            'REVIVAL': 'fas fa-church',
            'FELLOWSHIP': 'fas fa-handshake',
            'WEDDING': 'fas fa-ring',
            'PRAYER': 'fas fa-pray',
        }
        return icons.get(self.event_type, 'fas fa-calendar-alt')

    def get_event_class(self):
        return self.event_type.lower()

    def is_past_event(self):
        return self.date < timezone.now()

    def get_event_status(self):
        now = timezone.now()
        if self.date.date() == now.date():
            return 'today'
        elif self.date > now:
            return 'upcoming'
        else:
            return 'past'

    def get_event_badge_class(self):
        status = self.get_event_status()
        classes = {
            'upcoming': 'status-upcoming',
            'today': 'status-today', 
            'past': 'status-past'
        }
        return classes.get(status, 'status-upcoming')

    def get_event_badge_text(self):
        status = self.get_event_status()
        texts = {
            'upcoming': 'Upcoming',
            'today': 'Happening Today!',
            'past': 'Past Event'
        }
        return texts.get(status, 'Upcoming')
    
class Leader(models.Model):
    POSITION_CHOICES = [
        ('DIOCESE', 'Diocese Leader'),
        ('VICAR', 'Vicar'),
        ('ASSISTANT_VICAR', 'Assistant Vicar'),
        ('YOUTH_LEADER', 'Youth Ministry Leader'),
        ('MU_LEADER', 'Mothers Union Leader'),
        ('KAMA_LEADER', 'KAMA Leader'),
        ('SUNDAY_SCHOOL_LEADER', 'Sunday School Leader'),
        ('CHOIR_LEADER', 'Choir/Worship Leader'),
        ('TREASURER', 'Treasurer'),
        ('SECRETARY', 'Secretary'),
        ('ELDER', 'Church Elder'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    bio = models.TextField()
    image = models.ImageField(upload_to='leaders/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'position', 'name']
        verbose_name_plural = 'ALL CHURCH LEADERS'

    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"

    def get_absolute_url(self):
        return reverse('leader-detail', kwargs={'pk': self.pk})
    

# models.py - Add Gallery model
class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('SERVICES', 'Sunday Services'),
        ('EVENTS', 'Special Events'),
        ('OUTREACH', 'Community Outreach'),
        ('YOUTH', 'Youth Ministry'),
        ('WEDDING', 'Weddings'),
        ('REVIVAL', 'Revivals'),
        ('FELLOWSHIP', 'Fellowships'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='EVENTS')
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField(default=timezone.now, help_text="Date when the photo was taken")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date', '-created_at']
        verbose_name_plural = 'Church Gallery'

    def __str__(self):
        return self.title

    def formatted_date(self):
        """Returns formatted date like 'January 15, 2023'"""
        return self.event_date.strftime('%B %d, %Y')

    def get_category_class(self):
        """Returns CSS class for category"""
        return self.category.lower()

    def get_absolute_url(self):
        return reverse('gallery-detail', kwargs={'pk': self.pk})
    


class ChurchService(models.Model):
    SERVICE_TYPES = [
        ('kiswahili', 'Kiswahili Service'),
        ('english', 'English Service'),
        ('youth', 'Youth Service'),
        ('children', 'Children Service'),
        ('prayer', 'Prayer Service'),
    ]
    
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    schedule = models.CharField(max_length=100, help_text="e.g., Sundays at 8:00 AM")
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="External image URL if not uploading")
    youtube_playlist_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    # New fields for automatic past events
    last_service_date = models.DateField(blank=True, null=True, help_text="Date of the last service (auto-updated)")
    auto_generate_events = models.BooleanField(default=True, help_text="Automatically create past events from services")
    
    class Meta:
        ordering = ['order', 'service_type']
        verbose_name_plural = "Sermon Services"
    
    def __str__(self):
        return f"{self.name} - {self.schedule}"
    
    def get_image_url(self):
        """Return either uploaded image or external image URL"""
        if self.image:
            return self.image.url
        return self.image_url or ''
    
    def is_service_past_due(self):
        """Check if the service time has passed for today"""
        if not self.last_service_date:
            return False
        
        # If last service date is before today, it's past due
        return self.last_service_date < timezone.now().date()
    
    def create_past_event_from_service(self):
        """Create a SermonEvent from this service if it's past due"""
        if self.auto_generate_events and self.is_service_past_due() and self.last_service_date:
            # Check if event already exists for this service and date
            existing_event = SermonEvent.objects.filter(
                title__icontains=self.name,
                event_date=self.last_service_date
            ).exists()
            
            if not existing_event:
                event_title = f"{self.name} - {self.last_service_date.strftime('%B %d, %Y')}"
                
                SermonEvent.objects.create(
                    title=event_title,
                    event_type='other',  # Default type for service-based events
                    event_date=self.last_service_date,
                    description=f"Recorded service from {self.name}. {self.description}",
                    image=self.image,
                    image_url=self.image_url,
                    youtube_url=self.youtube_playlist_url,
                    is_active=True
                )
                return True
        return False

class SermonEvent(models.Model):
    EVENT_TYPES = [
        ('easter', 'Easter Celebration'),
        ('christmas', 'Christmas Service'),
        ('baptism', 'Baptism Service'),
        ('conference', 'Conference'),
        ('revival', 'Revival Meeting'),
        ('other', 'Other Event'),
        ('service', 'Regular Service'),  # New type for service-based events
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='sermon_events/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text="External image URL if not uploading")
    youtube_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    # Link to service if this event was auto-generated from a service
    source_service = models.ForeignKey(
        ChurchService, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        related_name='generated_events'
    )
    
    class Meta:
        ordering = ['-event_date', 'order']
        verbose_name_plural = "Update Past Sermons"
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"
    
    def formatted_date(self):
        """Return formatted date: Month Day, Year"""
        return self.event_date.strftime("%B %d, %Y")
    
    def get_image_url(self):
        """Return either uploaded image or external image URL"""
        if self.image:
            return self.image.url
        return self.image_url or ''
    
