from django.contrib import admin

from .models import (
    Profile,
    Extra,
)


class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'student_id',
        'name',
        'department',
        'clazz',
        'major',
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Extra)
