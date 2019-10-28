from django.contrib import admin
from sports.models import Sport, Tournaments, CoachingCenters


admin.site.register([Sport, Tournaments, CoachingCenters])
