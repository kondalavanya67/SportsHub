from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User
from shopping.models import Product


def phone_number_validation(ph_num):
    if len(str(ph_num)) != 10:
        raise ValidationError('The phone number must have 10 digits only')
    elif ph_num < 0:
        raise ValidationError('The phone number must be positive')


class Profile(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    prod = models.ManyToManyField(Product, blank=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user_name.username
