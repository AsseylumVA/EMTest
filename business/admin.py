from django.contrib import admin

from .models import BusinessElement

@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    pass
