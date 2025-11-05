# admin.py
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'location', 'is_upcoming', 'days_until_event']  # Changed to days_until_event
    list_filter = ['event_type', 'date']
    search_fields = ['title', 'description', 'location']
    ordering = ['date']

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'speaker', 'is_recent']
    list_filter = ['date', 'speaker']
    search_fields = ['title', 'description', 'speaker']
    date_hierarchy = 'date'

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