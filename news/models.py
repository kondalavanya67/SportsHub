from django.db import models
from django_unixdatetimefield import UnixDateTimeField


# Create your models here.

class HeadLine(models.Model):
    title = models.CharField(max_length=1000)
    image_url = models.TextField()
    url = models.TextField()
    site = models.TextField(default="asdf")
    time = models.TextField(default="wow")

    def __str__(self):
        return self.title


class LastNewsUpdate(models.Model):
    last_update = UnixDateTimeField()

    def __str__(self):
        return str(self.last_update)
