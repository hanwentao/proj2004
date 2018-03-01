import argparse
import pathlib
import shutil

from django.core.management.base import BaseCommand

import openpyxl

from ...models import Profile
from ...templatetags.contacts import gender


class Command(BaseCommand):
    help = 'Export card information.'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--template', required=True,
            type=argparse.FileType('rb'),
            help='Template file in Excel.')
        parser.add_argument('-o', '--output', required=True,
            type=argparse.FileType('wb'),
            help='Output file in Excel.')
        parser.add_argument('-p', '--photo',
            help='Path to export photos.')

    def handle(self, *args, **options):
        template_file = options['template']
        output_file = options['output']
        photo_folder_path = pathlib.Path(options['photo']) if options['photo'] else None
        profiles = {}
        num_nonempty = 0
        num_with_photo = 0
        for profile in Profile.objects.filter(user__is_active=True):
            profiles[profile.student_id] = profile
            if profile.completeness > 0:
                num_nonempty += 1
            if profile.user.extra.photo:
                num_with_photo += 1
                if photo_folder_path:
                    photo_path = photo_folder_path / f'{profile.student_id}.jpg'
                    with open(photo_path, 'wb') as photo_file:
                        shutil.copyfileobj(profile.user.extra.photo, photo_file)
        workbook = openpyxl.load_workbook(template_file)
        sheet = workbook.active
        row = 9  # XXX: hacking
        while True:
            student_id = sheet.cell(row=row, column=1).value
            if not student_id:
                break
            student_id = str(student_id)
            profile = profiles.get(student_id)
            if profile is not None:
                sheet.cell(row=row, column=7, value=profile.organization)
                sheet.cell(row=row, column=8, value=' '.join((profile.position, profile.title)))
                sheet.cell(row=row, column=9, value=str(profile.mobile))
                sheet.cell(row=row, column=10, value=profile.email)
                sheet.cell(row=row, column=11, value=profile.address)
                sheet.cell(row=row, column=12, value=profile.postcode)
                sheet.cell(row=row, column=13, value=profile.wechat)
                del profiles[student_id]
            row += 1
        for profile in sorted(profiles.values(), key=lambda p: p.student_id):
            if profile.completeness == 0:
                continue
            sheet.append([
                profile.student_id,
                profile.name,
                gender(profile.gender),
                profile.enroll_year,
                profile.department_name,
                profile.class_name,
                profile.organization,
                ' '.join((profile.position, profile.title)),
                str(profile.mobile),
                profile.email,
                profile.address,
                profile.postcode,
                profile.wechat,
            ])
        workbook.save(output_file)
        self.stdout.write(f'{num_nonempty} {num_with_photo}')
