from django.contrib import admin

from .models import (
    Department,
    Clazz,
    Profile,
    Extra,
)


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = [
        'code',
        'name',
    ]


class ClazzAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]


class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'student_id',
        'name',
        'department',
        'clazz',
        'major',
    ]

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Clazz, ClazzAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Extra)
