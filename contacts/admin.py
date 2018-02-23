from django.contrib import admin

from .models import (
    Department,
    Class,
    Profile,
    Extra,
)


class DepartmentAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'linkmen',
    )
    search_fields = (
        'code',
        'name',
    )


class ClassAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'linkmen',
    )
    search_fields = (
        'name',
        'department__name',
    )


class ProfileAdmin(admin.ModelAdmin):
    search_fields = [
        'student_id',
        'name',
        'major',
        'classes__name',
        'classes__department__name',
    ]

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Extra)
