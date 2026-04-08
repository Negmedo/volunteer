from django.contrib import admin
from .models import Profile, VolunteerProfile, VolunteerLanguage, VolunteerSkill, VolunteerAvailability
admin.site.register([Profile, VolunteerProfile, VolunteerLanguage, VolunteerSkill, VolunteerAvailability])
