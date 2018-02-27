import argparse
import csv
import sys

from django.core.management.base import BaseCommand

from ...models import (
    Class,
    Profile,
)


class Command(BaseCommand):
    help = 'Import new class information.'

    def add_arguments(self, parser):
        parser.add_argument('newclass', nargs='*', type=argparse.FileType(encoding='utf-8'), help='New class information file.')

    def handle(self, *args, **options):
        newclass_files = options['newclass'] if options['newclass'] else [sys.stdin]
        for newclass_file in newclass_files:
            csv_reader = csv.reader(newclass_file)
            for row in csv_reader:
                name, student_id, class_list = row
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
                for class_name in class_list.split():
                    try:
                        class_ = Class.objects.get(name=class_name)
                    except Class.DoesNotExist:
                        self.stderr.write(self.style.WARNING(f'Class {class_name} does not exist.'))
                        continue
                    profile.classes.add(class_)
                    self.stdout.write(self.style.SUCCESS(f'Added {name} to class {class_name}.'))
