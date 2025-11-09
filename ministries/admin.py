from django.contrib import admin
from .models import *

# Custom admin classes for better display
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry_type', 'leader_name', 'is_active', 'created_at']
    list_filter = ['ministry_type', 'is_active', 'created_at']
    search_fields = ['name', 'leader_name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'ministry_type', 'description', 'is_active')
        }),
        ('Leadership', {
            'fields': ('leader_name', 'leader_email', 'leader_phone')
        }),
        ('Meeting Details', {
            'fields': ('meeting_schedule', 'location')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry', 'day_of_week', 'time', 'location', 'is_recurring']
    list_filter = ['ministry', 'day_of_week', 'is_recurring']
    search_fields = ['name', 'description', 'ministry__name']
    list_editable = ['day_of_week', 'time', 'is_recurring']
    raw_id_fields = ['ministry']

class MinistryMemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'ministry', 'role', 'email', 'is_active', 'date_joined']
    list_filter = ['ministry', 'role', 'is_active', 'date_joined']
    search_fields = ['full_name', 'email', 'ministry__name']
    list_editable = ['role', 'is_active']
    raw_id_fields = ['user', 'ministry']
    readonly_fields = ['date_joined']

class InterestFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'ministry_type', 'email', 'submission_date', 'is_contacted']
    list_filter = ['ministry_type', 'is_contacted', 'submission_date']
    search_fields = ['full_name', 'email', 'message']
    list_editable = ['is_contacted']
    readonly_fields = ['submission_date']
    actions = ['mark_as_contacted']
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(is_contacted=True)
        self.message_user(request, f'{updated} submissions marked as contacted.')
    mark_as_contacted.short_description = "Mark selected submissions as contacted"


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 1
    ordering = ['order']

@admin.register(SundaySchoolSchedule)
class SundaySchoolScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'schedule_type', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['schedule_type', 'is_active']
    inlines = [ScheduleItemInline]

@admin.register(SundaySchoolTeacher)
class SundaySchoolTeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'age_group', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['age_group', 'is_active']
    search_fields = ['name', 'position']

@admin.register(SundaySchoolRegistration)
class SundaySchoolRegistrationAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'age_group', 'parent_name', 'phone', 'submitted_at', 'is_contacted']
    list_editable = ['is_contacted']
    list_filter = ['age_group', 'is_contacted', 'submitted_at']
    search_fields = ['child_name', 'parent_name', 'email']
    readonly_fields = ['submitted_at']

class InfoItemInline(admin.TabularInline):
    model = InfoItem
    extra = 1
    ordering = ['order']

@admin.register(SundaySchoolInfo)
class SundaySchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'info_type', 'is_active']
    list_editable = ['is_active']
    list_filter = ['info_type', 'is_active']
    inlines = [InfoItemInline]


@admin.register(MothersUnionActivity)
class MothersUnionActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'schedule']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

@admin.register(MothersUnionLeader)
class MothersUnionLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'position']

@admin.register(MothersUnionEvent)
class MothersUnionEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'time', 'location', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active', 'date']
    search_fields = ['title', 'description']

@admin.register(MothersUnionMembership)
class MothersUnionMembershipAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'created_at', 'is_contacted']
    list_filter = ['is_contacted', 'created_at']
    search_fields = ['full_name', 'email']
@admin.register(WeeklyProgram)
class WeeklyProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'program_type', 'day', 'time', 'is_active', 'order']
    list_filter = ['program_type', 'is_active']
    list_editable = ['is_active', 'order']

@admin.register(YouthEvent)
class YouthEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'is_upcoming']
    list_filter = ['is_upcoming', 'event_date']
    search_fields = ['title', 'description']

@admin.register(YouthLeader)
class YouthLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'is_active', 'order']
    list_editable = ['is_active', 'order']

@admin.register(YouthGallery)
class YouthGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'upload_date', 'is_active']
    list_filter = ['is_active', 'upload_date']

@admin.register(VisitorResource)
class VisitorResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'upload_date', 'is_active']
    list_editable = ['is_active']

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'time', 'location']
    list_filter = ['event_type', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'

class MinistryGalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'ministry', 'upload_date', 'is_featured']
    list_filter = ['ministry', 'is_featured', 'upload_date']
    search_fields = ['title', 'description', 'ministry__name']
    list_editable = ['is_featured']
    raw_id_fields = ['ministry']
    readonly_fields = ['upload_date']



@admin.register(KamaMotto)
class KamaMottoAdmin(admin.ModelAdmin):
    list_display = ['motto', 'is_active', 'created_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        # Only allow one active motto at a time
        if KamaMotto.objects.filter(is_active=True).exists():
            return False
        return True

@admin.register(KamaActivity)
class KamaActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'schedule']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

@admin.register(KamaLeader)
class KamaLeaderAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'position']


@admin.register(MusicMinistryTeam)
class MusicMinistryTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'team_type', 'leader_name', 'is_active', 'order']
    list_filter = ['team_type', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(MusicMinistryRegistration)
class MusicMinistryRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'team', 'experience', 'instrument', 'submitted_at', 'is_contacted']
    list_filter = ['team', 'experience', 'is_contacted', 'submitted_at']
    search_fields = ['full_name', 'phone', 'email']
    readonly_fields = ['submitted_at']
    list_editable = ['is_contacted']


# Register all models using the same method
admin.site.register(Ministry, MinistryAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(MinistryMember, MinistryMemberAdmin)
admin.site.register(InterestFormSubmission, InterestFormSubmissionAdmin)
admin.site.register(Event, EventAdmin)  # ONLY ONE registration


# Optional: Customize the admin header
admin.site.site_header = "Church Ministries Administration"
admin.site.site_title = "Church Ministries Admin"
admin.site.index_title = "Welcome to Church Ministries Admin"