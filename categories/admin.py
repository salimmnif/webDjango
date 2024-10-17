from django.contrib import admin
from .models import Category
class categoriesadmin(admin.ModelAdmin):
    search_fields=('title',)
# Register your models here.
