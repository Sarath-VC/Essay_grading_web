from django.contrib import admin
from .models import Topics, Bow, Essays, Report

# Register your models here.
admin.site.register(Topics)
admin.site.register(Bow)
admin.site.register(Essays)
admin.site.register(Report)