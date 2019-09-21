from django.db import models


# Create your models here.

class HeadLine(models.Model):
    title = models.CharField(max_length=1000)
    image_url = models.TextField()
    url = models.TextField()
    site = models.TextField(default="asdf")
    time = models.TextField(default="wow")

    def __str__(self):
        return self.title
