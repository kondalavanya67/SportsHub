from django.contrib import admin
from sports.models import Sport_Info, Tournaments, CoachingCenters


admin.site.register([Sport_Info, Tournaments, CoachingCenters])
