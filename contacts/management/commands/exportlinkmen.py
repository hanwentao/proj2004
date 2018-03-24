import csv

from django.core.management.base import BaseCommand

from ...models import Department, Profile


class Command(BaseCommand):
    help = 'Export linkmen information.'

    def add_arguments(self, parser):
        parser.add_argument('-C', '--without-class', action='store_true', help='Do not display class field.')
        parser.add_argument('id', nargs='*', help='Name or student id to display.')

    def handle(self, *args, **options):
        without_class = options['without_class']
        id_list = options['id']
        csv_writer = csv.writer(self.stdout)
        if without_class:
            csv_writer.writerow(['院系', '姓名', '手机', '邮箱'])
        else:
            csv_writer.writerow(['院系', '班级', '姓名', '手机', '邮箱'])
        if id_list:
            for id in id_list:
                if id.isdigit():
                    profile = Profile.objects.get(student_id=id)
                else:
                    profile = Profile.objects.get(name=id)
                if without_class:
                    csv_writer.writerow([profile.department_name, profile.name, profile.mobile, profile.email])
                else:
                    csv_writer.writerow([profile.department_name, profile.class_name, profile.name, profile.mobile, profile.email])
        else:
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
