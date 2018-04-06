from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

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
    search_fields = (
        'student_id',
        'name',
        'major',
        'classes__name',
        'classes__department__name',
    )
    list_display = (
        'student_id',
        'name',
        'class_name',
        'extra',
    )
    list_display_links = (
        'student_id',
        'name',
    )

    def class_name(self, obj):
        return obj.class_name
    class_name.short_description = '班级'

    def extra(self, obj):
        return format_html('<a href="{}">额外信息</a>',
            reverse('admin:contacts_extra_change', args=(obj.user.extra.id,)))
    extra.short_description = '额外信息'


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Extra)
