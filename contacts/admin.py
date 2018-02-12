from django.contrib import admin

from .models import (
    Department,
    Clazz,
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


class ClazzAdmin(admin.ModelAdmin):
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
        'clazzes__name',
        'clazzes__department__name',
    ]

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Clazz, ClazzAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Extra)
