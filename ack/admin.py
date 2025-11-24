# admin.py
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.db.models import Count

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'location', 'is_upcoming', 'days_until_event']  # Changed to days_until_event
    list_filter = ['event_type', 'date']
    search_fields = ['title', 'description', 'location']
    ordering = ['date']
    eadonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']
    search_fields = ['name', 'bio']
    list_editable = ['order', 'is_active']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'event_date', 'is_featured', 'created_at']
    list_filter = ['category', 'event_date', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    date_hierarchy = 'event_date'
    
    # Add image preview
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: cover;" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'


@admin.register(ChurchService)
class ChurchServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'service_type', 
        'schedule', 
        'last_service_date', 
        'auto_generate_events',  # ADD THIS LINE
        'is_service_past_due', 
        'is_active', 
        'order'
    ]
    list_filter = ['service_type', 'is_active', 'auto_generate_events']
    list_editable = [
        'is_active', 
        'order', 
        'auto_generate_events',  # Now this is valid since it's in list_display
        'last_service_date'
    ]
    search_fields = ['name', 'description']
    actions = ['generate_past_events']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service_type', 'schedule', 'description')
        }),
        ('Media & Links', {
            'fields': ('image', 'image_url', 'youtube_playlist_url')
        }),
        ('Automatic Event Generation', {
            'fields': ('auto_generate_events', 'last_service_date'),
            'description': 'Set the last service date and enable auto-generation to create past events automatically.'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def generate_past_events(self, request, queryset):
        """Admin action to manually generate past events from selected services"""
        created_count = 0
        for service in queryset:
            if service.create_past_event_from_service():
                created_count += 1
        
        if created_count:
            self.message_user(request, f"Successfully created {created_count} past events.")
        else:
            self.message_user(request, "No new past events were created.")
    
    generate_past_events.short_description = "Generate past events from selected services"


@admin.register(SermonEvent)
class SermonEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'source_service', 'is_active', 'order']
    list_filter = ['event_type', 'is_active', 'event_date', 'source_service']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'description']
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'event_type', 'event_date', 'description', 'source_service')
        }),
        ('Media & Links', {
            'fields': ('image', 'image_url', 'youtube_url')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )



@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at', 'short_message']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Review Management', {
            'fields': ('status', 'admin_notes')
        }),
    )
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(status='read')
    mark_as_read.short_description = "Mark selected reviews as read"
    
    def mark_as_replied(self, request, queryset):
        queryset.update(status='replied')
    mark_as_replied.short_description = "Mark selected reviews as replied"


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        review_stats = CustomerReview.objects.aggregate(
            total=Count('id'),
            unread=Count('id', filter=models.Q(status='unread')),
            read=Count('id', filter=models.Q(status='read')),
        )
        extra_context['review_stats'] = review_stats
        return super().index(request, extra_context)