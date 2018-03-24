import csv

from django.core.management.base import BaseCommand

from ...models import Department


class Command(BaseCommand):
    help = 'Export linkmen information.'

    def add_arguments(self, parser):
        parser.add_argument('-C', '--without-class', action='store_true')

    def handle(self, *args, **options):
        without_class = options['without_class']
        csv_writer = csv.writer(self.stdout)
        if without_class:
            csv_writer.writerow(['院系', '姓名', '手机', '邮箱'])
        else:
            csv_writer.writerow(['院系', '班级', '姓名', '手机', '邮箱'])
        for department in Department.objects.all():
            for user in department.linkmen.all():
                profile = user.profile
                if without_class:
                    csv_writer.writerow([department.name, profile.name, profile.mobile, profile.email])
                else:
                    csv_writer.writerow([department.name, '', profile.name, profile.mobile, profile.email])
            if without_class:
                continue
            for class_ in department.class_set.all():
                for user in class_.linkmen.all():
                    profile = user.profile
                    csv_writer.writerow([department.name, class_.name, profile.name, profile.mobile, profile.email])

