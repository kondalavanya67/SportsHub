from django.contrib import admin
from shopping.models import Category, Product

admin.site.register([Category, Product])
