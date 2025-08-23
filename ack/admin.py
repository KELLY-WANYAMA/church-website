from django.contrib import admin
from .models import Sermon, Event  # Only import the models you have now

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'speaker')
    search_fields = ('title', 'speaker')
    list_filter = ('date',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'event_type')
    search_fields = ('title', 'location')
    list_filter = ('date', 'event_type')



