from django.db import models
from datetime import date
from django.utils import timezone
from django.urls import reverse


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=date.today)
    speaker = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=date.today)
    location = models.CharField(max_length=200)
    description = models.TextField()
    
    EVENT_TYPES = [
        ('REVIVAL', 'Revival'),
        ('FELLOWSHIP', 'Fellowship'),
        ('WEDDING', 'Wedding'),
        ('PRAYER', 'Prayer'),
    ]
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='FELLOWSHIP')

    def __str__(self):
        return self.title