import argparse
import csv
import sys

from django.core.management.base import BaseCommand

from ...models import (
    Department,
    Clazz,
    Profile,
)


class Command(BaseCommand):
    help = 'Import linkmen information.'

    def add_arguments(self, parser):
        parser.add_argument('linkmen', nargs='*', type=argparse.FileType(encoding='utf-8'), help='Linkmen data file.')

    def handle(self, *args, **options):
        linkmen_files = options['linkmen'] if options['linkmen'] else [sys.stdin]
        for linkmen_file in linkmen_files:
            csv_reader = csv.reader(linkmen_file)
            for row in csv_reader:
                name, student_id, department_list, class_list = row
                try:
                    if student_id:
                        profile = Profile.objects.get(student_id=student_id)
                    else:
                        profile = Profile.objects.get(name=name)
                    user = profile.user
                except Profile.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'{student_id} {name} does not exist.'))
                    continue
                except Profile.MultipleObjectsReturned:
                    self.stderr.write(self.style.WARNING(f'{name} duplicated.'))
                    continue
                for department_name in department_list.split():
                    try:
                        department = Department.objects.get(name=department_name)
                    except Department.DoesNotExist:
                        self.stderr.write(self.style.WARNING(f'Department {department_name} does not exist.'))
                        continue
                    department.linkmen.add(user)
                    self.stdout.write(self.style.SUCCESS(f'Added {name} to department {department_name}.'))
                for class_name in class_list.split():
                    try:
                        class_ = Clazz.objects.get(name=class_name)
                    except Clazz.DoesNotExist:
                        self.stderr.write(self.style.WARNING(f'Class {class_name} does not exist.'))
                        continue
                    class_.linkmen.add(user)
                    self.stdout.write(self.style.SUCCESS(f'Added {name} to class {class_name}.'))
