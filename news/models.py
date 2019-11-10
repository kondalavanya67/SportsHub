from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.

class HeadLine(models.Model):
    title = models.CharField(max_length=1000)
    image_url = models.TextField(null=True)
    url = models.TextField(null=True)
    site = models.TextField(null=True)
    time = models.TextField(null=True)
    category = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.title


class LastNewsUpdate(models.Model):
    last_update = UnixDateTimeField()

    def __str__(self):
        return str(self.last_update)
