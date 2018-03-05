import csv

from django.core.management.base import BaseCommand

from ...models import Department


class Command(BaseCommand):
    help = 'Export linkmen information.'

    def handle(self, *args, **options):
        csv_writer = csv.writer(self.stdout)
        csv_writer.writerow(['院系', '班级', '姓名', '邮箱'])
        for department in Department.objects.all():
            for user in department.linkmen.all():
                profile = user.profile
                csv_writer.writerow([department.name, '', profile.name, profile.email])
            for class_ in department.class_set.all():
                for user in class_.linkmen.all():
                    profile = user.profile
                    csv_writer.writerow([department.name, class_.name, profile.name, profile.email])

