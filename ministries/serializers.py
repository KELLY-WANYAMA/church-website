from rest_framework import serializers
from django.utils import timezone
from .models import *


class ProgramSerializer(serializers.ModelSerializer):
    formatted_schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = Program
        fields = [
            'id', 'name', 'description', 'day_of_week', 'time', 'location',
            'target_audience', 'is_recurring', 'frequency', 'formatted_schedule'
        ]
    
    def get_formatted_schedule(self, obj):
        if obj.day_of_week and obj.time:
            return f"{obj.day_of_week}s, {obj.time}"
        return obj.time


class MinistryMemberSerializer(serializers.ModelSerializer):
    membership_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = MinistryMember
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'role',
            'date_joined', 'is_active', 'membership_duration'
        ]
        read_only_fields = ['id']
    
    def get_membership_duration(self, obj):
        """Calculate how long someone has been a member"""
        duration = timezone.now().date() - obj.date_joined
        return f"{duration.days // 30} months"


class MinistryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing ministries"""
    program_count = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    active_programs = serializers.SerializerMethodField()
    
    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'ministry_type', 'description', 'leader_name',
            'meeting_schedule', 'location', 'program_count', 'member_count', 'active_programs'
        ]
    
    def get_program_count(self, obj):
        return obj.programs.count()
    
    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()
    
    def get_active_programs(self, obj):
        return list(obj.programs.values_list('name', flat=True)[:3])


class MinistryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single ministry view"""
    programs = ProgramSerializer(many=True, read_only=True)
    members = MinistryMemberSerializer(many=True, read_only=True)
    upcoming_events = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Ministry
        fields = [
            'id', 'name', 'ministry_type', 'description', 'leader_name',
            'leader_email', 'leader_phone', 'meeting_schedule', 'location',
            'is_active', 'created_at', 'programs', 'members', 'gallery',
            'upcoming_events', 'contact_info'
        ]
    
    def get_upcoming_events(self, obj):
        upcoming = obj.events.filter(date__gte=timezone.now().date())[:5]
        return MinistryEventSerializer(upcoming, many=True).data
    
    def get_contact_info(self, obj):
        return {
            'leader': obj.leader_name,
            'email': obj.leader_email,
            'phone': obj.leader_phone
        }


class MinistryEventSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()
    is_upcoming = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'formatted_date',
            'start_time', 'end_time', 'formatted_time', 'location',
            'is_public', 'max_attendees', 'is_upcoming'
        ]
    
    def get_formatted_date(self, obj):
        return obj.date.strftime("%A, %B %d, %Y")
    
    def get_formatted_time(self, obj):
        if obj.end_time:
            return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"
        return obj.start_time.strftime('%I:%M %p')
    
    def get_is_upcoming(self, obj):
        return obj.date >= timezone.now().date()


class InterestFormSubmissionSerializer(serializers.ModelSerializer):
    days_ago = serializers.SerializerMethodField()
    ministry_display_name = serializers.SerializerMethodField()
    requires_followup = serializers.SerializerMethodField()
    
    class Meta:
        model = InterestFormSubmission
        fields = [
            'id', 'ministry_type', 'ministry_display_name', 'full_name',
            'email', 'phone_number', 'message', 'submission_date',
            'is_contacted', 'contact_notes', 'contact_date',
            'days_ago', 'requires_followup'
        ]
        read_only_fields = ['id', 'submission_date']
    
    def get_days_ago(self, obj):
        return (timezone.now() - obj.submission_date).days
    
    def get_ministry_display_name(self, obj):
        return obj.get_ministry_type_display()
    
    def get_requires_followup(self, obj):
        return not obj.is_contacted and (timezone.now() - obj.submission_date).days <= 7
    
    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError("Phone number should start with country code (e.g., +254)")
        return value


class InterestFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestFormSubmission
        fields = [
            'ministry_type', 'full_name', 'email', 'phone_number', 'message'
        ]
    
    def create(self, validated_data):
        # Add any custom logic before saving
        return super().create(validated_data)


# Dashboard Statistics Serializers
class MinistryStatsSerializer(serializers.Serializer):
    total_ministries = serializers.IntegerField()
    active_members = serializers.IntegerField()
    total_programs = serializers.IntegerField()
    pending_interest_forms = serializers.IntegerField()
    recent_submissions = InterestFormSubmissionSerializer(many=True)


class MinistryTypeStatsSerializer(serializers.Serializer):
    ministry_type = serializers.CharField()
    display_name = serializers.CharField()
    count = serializers.IntegerField()
    active_programs = serializers.IntegerField()