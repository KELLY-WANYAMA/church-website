from rest_framework import serializers
from .models import Sermon, Event
from django.utils import timezone


class SermonSerializer(serializers.ModelSerializer):
    # Custom fields for enhanced API response
    formatted_date = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    days_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Sermon
        fields = [
            'id', 'title', 'date', 'formatted_date', 'speaker', 
            'description', 'video_url', 'is_recent', 'days_ago',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_formatted_date(self, obj):
        """Return formatted date for API responses"""
        return obj.date.strftime("%B %d, %Y")
    
    def get_is_recent(self, obj):
        """Use the model method"""
        return obj.is_recent()
    
    def get_days_ago(self, obj):
        """Calculate how many days ago the sermon was"""
        delta = timezone.now().date() - obj.date
        return delta.days
    
    def validate_date(self, value):
        """Ensure sermon date is not in the future"""
        if value > timezone.now().date():
            raise serializers.ValidationError("Sermon date cannot be in the future")
        return value


class EventSerializer(serializers.ModelSerializer):
    # Custom fields for better API response
    formatted_date = serializers.SerializerMethodField()
    formatted_event_type = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    days_until_event = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'formatted_date', 'location', 
            'description', 'event_type', 'formatted_event_type',
            'is_upcoming', 'days_until_event', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_formatted_date(self, obj):
        """Return formatted date for API responses"""
        return obj.date.strftime("%B %d, %Y at %I:%M %p")
    
    def get_formatted_event_type(self, obj):
        """Return human-readable event type"""
        return obj.get_event_type_display()
    
    def get_is_upcoming(self, obj):
        """Use the model method"""
        return obj.is_upcoming()
    
    def get_days_until_event(self, obj):
        """Use the model method"""
        return obj.days_until_event()
    
    def validate_date(self, value):
        """Ensure event date is reasonable"""
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value


# Optimized serializers for list views
class SermonListSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    
    class Meta:
        model = Sermon
        fields = ['id', 'title', 'formatted_date', 'speaker', 'video_url', 'is_recent']
    
    def get_formatted_date(self, obj):
        return obj.date.strftime("%b %d, %Y")
    
    def get_is_recent(self, obj):
        return obj.is_recent()


class EventListSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()
    formatted_event_type = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'formatted_date', 'location', 'event_type', 'formatted_event_type', 'is_upcoming']
    
    def get_formatted_date(self, obj):
        return obj.date.strftime("%b %d, %Y at %I:%M %p")
    
    def get_formatted_event_type(self, obj):
        return obj.get_event_type_display()
    
    def get_is_upcoming(self, obj):
        return obj.is_upcoming()