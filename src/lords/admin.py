from django.contrib import admin
from lords import models

class LordAdmin(admin.ModelAdmin):
    list_display = ['user', 'family', 'gold', 'army']

admin.site.register(models.Lord, LordAdmin)