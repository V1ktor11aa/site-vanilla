from django.contrib import admin
from .models import Coffee

class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'prise', 'quantity')

admin.site.register(Coffee, CoffeeAdmin)