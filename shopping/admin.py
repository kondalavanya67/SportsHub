from django.contrib import admin
from shopping.models import Category, Product, Review

admin.site.register([Category, Product, Review])
