# models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    speaker = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def is_recent(self):
        """Check if sermon is from last 30 days"""
        return (timezone.now().date() - self.date).days <= 30

    def get_absolute_url(self):
        return reverse('sermon-detail', kwargs={'pk': self.pk})


# models.py - update your Event model
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
        verbose_name_plural = 'Gallery Items'

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