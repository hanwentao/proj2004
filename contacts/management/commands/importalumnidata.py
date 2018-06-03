import argparse
import csv
import datetime
import sys

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from ...models import (
    Department,
    Class,
    Profile,
    Extra,
)

def create_user_with_basic_info(student_id, name, gender, dob, enroll_year, graduate_year, department_name, major, class_name, department_code):
    user, created = User.objects.get_or_create(username=student_id)
    profile, _ = Profile.objects.get_or_create(user=user)
    extra, _ = Extra.objects.get_or_create(user=user)
    profile.student_id = student_id
    profile.name = name
    profile.gender = gender
    profile.dob = dob
    profile.enroll_year = enroll_year
    profile.graduate_year = graduate_year
    department, _ = Department.objects.update_or_create(name=department_name, defaults={
        'code': department_code,
    })
    class_, _ = Class.objects.update_or_create(name=class_name, defaults={
        'department': department,
    })
    profile.major = major
    profile.save()
    profile.classes.add(class_)
    return created


class Command(BaseCommand):
    help = 'Import alumni data.'

    def add_arguments(self, parser):
        parser.add_argument('-w', '--with-header', action='store_true', help='Specifies that input has header row.')
        parser.add_argument('alumni', nargs='*', type=argparse.FileType(), help='Alumni data file.')

    def handle(self, *args, **options):
        alumni = options['alumni'] if options['alumni'] else [sys.stdin]
        with_header = options['with_header']
        num_alumni_created = 0
        num_alumni_updated = 0
        for csv_file in alumni:
            csv_reader = csv.reader(csv_file)
            first = True
            for row in csv_reader:
                if first:
                    first = False
                    if with_header:
                        continue
                department_code, department, student_id, name, gender, dob, class_, major, enroll_date, graduate_date, grade, graduate_category = row
                gender = 'M' if gender == '男' else 'F'
                try:
                    dob = datetime.datetime.strptime(dob, '%Y%m%d').date()
                except ValueError:
                    dob = None
                try:
                    enroll_year = int(enroll_date[:4])
                except ValueError:
                    enroll_year = 2004
                try:
                    graduate_year = int(graduate_date[:4])
                except ValueError:
                    graduate_year = 2008
                if create_user_with_basic_info(student_id, name, gender, dob, enroll_year, graduate_year, department, major, class_, department_code):
                    num_alumni_created += 1
                else:
                    num_alumni_updated += 1
                if (num_alumni_created + num_alumni_updated) % 100 == 0:
                    self.stdout.write(f'Importing... {num_alumni_created} created, {num_alumni_updated} updated.')
        self.stdout.write(f'Done. {num_alumni_created} created, {num_alumni_updated} updated.')
