from django.contrib import admin
from sports.models import Sport, Tournaments


admin.site.register([Sport, Tournaments])
