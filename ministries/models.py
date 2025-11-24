# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.conf import settings

class Ministry(models.Model):
    MINISTRY_TYPES = [
        ('youth', 'Youth Ministry'),
        ('children', 'Children Ministry'),
        ('women', "Mother's Union"),
        ('men', 'KAMA - Men Ministry'),
        ('choir', 'Choir & Worship Ministry'),
        ('other', 'Other Ministry'),
    ]
    
    name = models.CharField(max_length=100)
    ministry_type = models.CharField(max_length=20, choices=MINISTRY_TYPES)
    description = models.TextField()
    leader_name = models.CharField(max_length=100, blank=True)
    leader_email = models.EmailField(blank=True)
    leader_phone = models.CharField(max_length=15, blank=True)
    meeting_schedule = models.TextField(help_text="Regular meeting days and times")
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Ministries"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Program(models.Model):
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=100)
    description = models.TextField()
    day_of_week = models.CharField(max_length=20, blank=True)
    time = models.CharField(max_length=50, help_text="e.g., Sundays, 9:30-10:30am")
    location = models.CharField(max_length=200)
    target_audience = models.CharField(max_length=100, blank=True)
    is_recurring = models.BooleanField(default=True)
    frequency = models.CharField(max_length=50, default='Weekly', help_text="e.g., Weekly, Monthly, Bi-weekly")
    
    class Meta:
        ordering = ['ministry', 'day_of_week', 'time']
    
    def __str__(self):
        return f"{self.ministry.name} - {self.name}"




class SundaySchoolSchedule(models.Model):
    SCHEDULE_TYPES = [
        ('regular', 'Regular Sunday Schedule'),
        ('special', 'Special Activities'),
    ]
    
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    title = models.CharField(max_length=200, help_text="e.g., Sunday Schedule, Special Activities")
    description = models.TextField(blank=True, null=True, help_text="Optional description")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Sunday School Schedules"
        ordering = ['order', 'schedule_type']
    
    def __str__(self):
        return f"{self.get_schedule_type_display()} - {self.title}"

class ScheduleItem(models.Model):
    schedule = models.ForeignKey(SundaySchoolSchedule, on_delete=models.CASCADE, related_name='items')
    time = models.CharField(max_length=100, help_text="e.g., 9:00 AM, 1st Sunday, Monthly")
    activity = models.CharField(max_length=200, help_text="e.g., Arrival & Welcome, Family Service")
    description = models.TextField(blank=True, null=True, help_text="Optional detailed description")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['schedule', 'order', 'time']
    
    def __str__(self):
        return f"{self.time} - {self.activity}"

class SundaySchoolTeacher(models.Model):
    AGE_GROUPS = [
        ('nursery', 'Nursery (3-5 years)'),
        ('primary', 'Primary (6-9 years)'),
        ('juniors', 'Juniors (10-12 years)'),
    ]
    
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, help_text="e.g., Nursery Class Teacher")
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sunday_school/teachers/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'age_group', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class SundaySchoolRegistration(models.Model):
    AGE_GROUPS = [
        ('nursery', 'Nursery (3-5 years)'),
        ('primary', 'Primary (6-9 years)'),
        ('juniors', 'Juniors (10-12 years)'),
    ]
    
    child_name = models.CharField(max_length=200)
    child_age = models.IntegerField()
    age_group = models.CharField(max_length=20, choices=AGE_GROUPS)
    parent_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    special_notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.child_name} - {self.age_group}"

class SundaySchoolInfo(models.Model):
    INFO_TYPES = [
        ('why_join', 'Why Join Us'),
        ('requirements', 'Requirements'),
    ]
    
    info_type = models.CharField(max_length=20, choices=INFO_TYPES)
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Sunday School Information"
    
    def __str__(self):
        return f"{self.get_info_type_display()} - {self.title}"

class InfoItem(models.Model):
    info = models.ForeignKey(SundaySchoolInfo, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=300)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['info', 'order']
    
    def __str__(self):
        return self.text

class MothersUnionActivity(models.Model):
    title = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=100, help_text="Font Awesome icon class (e.g., fas fa-praying-hands)")
    description = models.TextField()
    schedule = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Every Wednesday, 2:00 PM")
    location = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Order of display")
    
    class Meta:
        verbose_name_plural = "Mothers Union Activities"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class MothersUnionLeader(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='mothers_union/leaders/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of display")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'position']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

# Renamed to avoid conflict with existing Event model
class MothersUnionEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Mothers Union Events"
        ordering = ['date']
    
    def __str__(self):
        return self.title
    
    @property
    def display_date(self):
        return {
            'month': self.date.strftime('%b').upper(),
            'day': self.date.strftime('%d')
        }

class MothersUnionMembership(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    message = models.TextField()
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Mothers Union Memberships"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.created_at.strftime('%Y-%m-%d')}"
        

class MinistryMember(models.Model):
    MEMBER_ROLES = [
        ('leader', 'Leader'),
        ('assistant_leader', 'Assistant Leader'),
        ('member', 'Member'),
        ('volunteer', 'Volunteer'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='members')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+254...'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role = models.CharField(max_length=20, choices=MEMBER_ROLES, default='member')
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['email', 'ministry']
        ordering = ['ministry', 'role', 'full_name']
    
    def __str__(self):
        return f"{self.full_name} - {self.ministry.name}"


# # class Event(models.Model):
#     ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE, related_name='events')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField(null=True, blank=True)
#     location = models.CharField(max_length=200)
#     is_public = models.BooleanField(default=True)
#     max_attendees = models.PositiveIntegerField(null=True, blank=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     
#     class Meta:
#         ordering = ['date', 'start_time']
#     
#     def __str__(self):
        return f"{self.title} - {self.date}"


# Weekly Programs Model
class WeeklyProgram(models.Model):
    PROGRAM_TYPES = [
        ('youth_bonding', 'Team Bonding'),
        ('youth_night', 'Youth Night Kesha'),
        ('small_groups', 'Small Team Building'),
        ('Bible_Study', 'Bible Study'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    description = models.TextField()
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    icon_class = models.CharField(max_length=50, default='fas fa-heart')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Youth Weekly Programs"

    
    def __str__(self):
        return self.name

# Youth Events Model
class YouthEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    about_event = models.TextField(blank=True, null=True)
    what_to_bring = models.TextField(blank=True, null=True)
    cost = models.CharField(max_length=100, blank=True, null=True)
    age_group = models.CharField(max_length=100, blank=True, null=True)
    dress_code = models.CharField(max_length=100, blank=True, null=True)
    transportation_info = models.TextField(blank=True, null=True)
    is_upcoming = models.BooleanField(default=True)
    registration_required = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, null=True)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return self.title
    
    def formatted_date(self):
        return self.event_date.strftime("%b %d")
    
    def formatted_month(self):
        return self.event_date.strftime("%b").upper()
    
    def formatted_day(self):
        return self.event_date.strftime("%d")

# Youth Leaders Model
class YouthLeader(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='youth_leaders/')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

# Youth Gallery Model
class YouthGallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='youth_gallery/')
    description = models.TextField(blank=True, null=True)
    event_related = models.ForeignKey(YouthEvent, on_delete=models.SET_NULL, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name_plural = "Youth Galleries"
    
    def __str__(self):
        return self.title

#//CHANGED TO VISITORS RESOURCES IN YOUTH TEMPLATE
# Parent Resources Model// CHANGED TO VISITORS RESOURCES
class VisitorResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(
        upload_to='visitor_resources/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

#//COMMENTED THIS IN YOUTH TEMPLATE
# Parent Subscription Model
#class ParentSubscription(models.Model):
#    email = models.EmailField(unique=True)
#    subscribed_at = models.DateTimeField(auto_now_add=True)
#    is_active = models.BooleanField(default=True)
    
#    def __str__(self):
#        return self.email


# Utility functions to create sample data
def create_sample_ministries():
    """Create sample ministry data"""
    ministries_data = [
        {
            'name': 'IGNITE Youth',
            'ministry_type': 'youth',
            'description': 'Our vibrant youth community for teens ages 12-18',
            'leader_name': 'Youth Leader',
            'leader_email': 'youth@church.org',
            'meeting_schedule': 'Sundays and Wednesdays',
            'location': 'Youth Room and Main Hall'
        },
        {
            'name': "Mother's Union ACK",
            'ministry_type': 'women',
            'description': "Women's ministry focused on family values and community service",
            'leader_name': 'MU Leader',
            'leader_email': 'mothersunion@church.org',
            'meeting_schedule': 'Wednesdays and Monthly meetings',
            'location': 'Church Chapel and Various Locations'
        },
        {
            'name': 'KAMA - Men Ministry',
            'ministry_type': 'men',
            'description': 'Kenya Anglican Men Association focused on spiritual growth and service',
            'leader_name': 'KAMA Leader',
            'leader_email': 'kama@church.org',
            'meeting_schedule': 'Weekly and Monthly meetings',
            'location': 'Church Hall'
        },
        {
            'name': 'ACK Music Ministry',
            'ministry_type': 'choir',
            'description': 'Music ministry leading worship through choir and contemporary praise',
            'leader_name': 'Choir Director',
            'leader_email': 'choir@church.org',
            'meeting_schedule': 'Weekly practices and Sunday services',
            'location': 'Choir Loft'
        },
    ]
    
    for data in ministries_data:
        ministry, created = Ministry.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        
        if created:
            print(f"Created ministry: {ministry.name}")

def create_sample_programs():
    """Create sample program data"""
    try:
        youth_ministry = Ministry.objects.get(name='IGNITE Youth')
        mothers_union = Ministry.objects.get(name="Mother's Union ACK")
        
        programs_data = [
            {
                'ministry': youth_ministry,
                'name': 'Sunday School',
                'description': 'Bible study and discussion groups',
                'day_of_week': 'Sunday',
                'time': 'Sundays, 9:30-10:30am',
                'location': 'Youth Room',
                'target_audience': 'Youth 12-18 years'
            },
            {
                'ministry': youth_ministry,
                'name': 'Youth Night',
                'description': 'Worship, games, and relevant messages',
                'day_of_week': 'Wednesday',
                'time': 'Wednesdays, 7-9pm',
                'location': 'Main Hall',
                'target_audience': 'Youth 12-18 years'
            },
            {
                'ministry': mothers_union,
                'name': 'Weekly Prayer Meeting',
                'description': 'Intercessory prayer for families',
                'day_of_week': 'Wednesday',
                'time': 'Wednesdays, 2:00 PM',
                'location': 'Church Chapel',
                'target_audience': 'Women'
            },
            {
                'ministry': mothers_union,
                'name': 'Family Support',
                'description': 'Community outreach and counseling',
                'day_of_week': '',
                'time': 'Monthly',
                'location': 'Various Locations',
                'target_audience': 'Women and Families'
            },
        ]
        
        for data in programs_data:
            program, created = Program.objects.get_or_create(
                ministry=data['ministry'],
                name=data['name'],
                defaults=data
            )
            
            if created:
                print(f"Created program: {program.name}")
                
    except Ministry.DoesNotExist:
        print("Please create ministries first using create_sample_ministries()")
     


class KamaMotto(models.Model):
    motto = models.TextField(help_text="KAMA motto e.g., 'Men of Faith, Men of Action, Men of Service'")
    description = models.TextField(blank=True, help_text="Optional description of the motto")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "KAMA Motto"
    
    def __str__(self):
        return f"KAMA Motto: {self.motto[:50]}..."

class KamaActivity(models.Model):
    title = models.CharField(max_length=200)
    icon_class = models.CharField(max_length=100, help_text="Font Awesome icon class (e.g., fas fa-calendar-alt)")
    schedule = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Every 1st Saturday, 9:00 AM")
    description = models.TextField(help_text="Main description of the activity")
    additional_info = models.TextField(blank=True, null=True, help_text="Additional details or bullet points")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Order of display")
    
    class Meta:
        verbose_name_plural = "KAMA Activities"
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class KamaLeader(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='kama/leaders/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Order of display")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "KAMA Leaders"
        ordering = ['order', 'position']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


##THIS IS FOR KAMA
class InterestFormSubmission(models.Model):
    MINISTRY_CHOICES = [
        ('mothers_union', "Mother's Union"),
        ('kama', 'KAMA - Men Ministry'),
        ('youth', 'Youth Ministry'),
        ('children', 'Children Ministry'),
        ('choir', 'Choir & Worship'),
        ('other', 'Other'),
    ]
    
    ministry_type = models.CharField(max_length=20, choices=MINISTRY_CHOICES)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17, blank=True)
    message = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    contact_notes = models.TextField(blank=True)
    contact_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submission_date']
        verbose_name_plural = "KAMA Membership Interest"
    
    def __str__(self):
        return f"{self.full_name} - {self.get_ministry_type_display()} - {self.submission_date.strftime('%Y-%m-%d')}"
    
    def mark_contacted(self, notes=""):
        self.is_contacted = True
        self.contact_notes = notes
        self.contact_date = timezone.now()
        self.save()


# models.py
class MusicMinistryTeam(models.Model):
    TEAM_CHOICES = [
        ('choir', 'Choir Team'),
        ('praise', 'Praise & Worship Team'),
        ('both', 'Both Teams'),
    ]
    
    name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=20, choices=TEAM_CHOICES)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default='fas fa-microphone-alt')
    youtube_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    leader_name = models.CharField(max_length=100)
    leader_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class MusicMinistryRegistration(models.Model):
    EXPERIENCE_CHOICES = [
        ('none', 'No formal experience'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('professional', 'Professional'),
    ]
    
    INSTRUMENT_CHOICES = [
        ('soprano', 'Soprano (Choir)'),
        ('alto', 'Alto (Choir)'),
        ('tenor', 'Tenor (Choir)'),
        ('bass', 'Bass (Choir)'),
        ('guitar', 'Guitar'),
        ('piano', 'Piano/Keyboard'),
        ('drums', 'Drums'),
        ('bass_guitar', 'Bass Guitar'),
        ('other', 'Other Instrument'),
    ]
    
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    team = models.CharField(max_length=20, choices=MusicMinistryTeam.TEAM_CHOICES)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    instrument = models.CharField(max_length=20, choices=INSTRUMENT_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_team_display()}"