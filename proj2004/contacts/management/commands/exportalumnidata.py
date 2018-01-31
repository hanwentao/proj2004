import argparse
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import Profile


class Command(BaseCommand):
    help = 'Export alumni data.'

    def add_arguments(self, parser):
        parser.add_argument('-W', '--without-header', action='store_true', help='Specifies that output has no header row.')
        parser.add_argument('-u', '--with-url', action='store_true', help='Specifies that output has url column.')
        parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Outputs to file.')

    def handle(self, *args, **options):
        with_header = not options['without_header']
        with_url = options['with_url']
        out = options['output']
        if not out:
            out = sys.stdout
        writer = csv.writer(out)
        if with_header:
            writer.writerow([
                '姓名', '性别', '出生日期', '学号', '入学年', '毕业年', '院系', '专业', '班级',
                '工作单位、职务/职称', '所在行业',
                '手机', '固定电话', '电子邮箱', '微信号', '所在地区', '通讯地址', '邮编',
                '是否开通校友邮箱', '是否办理校友卡',
            ] + (['URL'] if with_url else []))
        num_alumni = 0
        for profile in Profile.objects.order_by('student_id'):
            writer.writerow([
                profile.name,
                '男' if profile.gender == 'M' else '女',
                profile.dob.strftime('%Y%m%d') if profile.dob is not None else '',
                profile.student_id,
                profile.enroll_year,
                profile.graduate_year,
                profile.department,
                profile.major,
                profile.clazz,
                ' '.join((profile.organization, profile.position, profile.title)),
                profile.industry,
                profile.mobile,
                profile.telephone,
                profile.email,
                profile.wechat,
                profile.location,
                profile.address,
                profile.postcode,
                '',
                '',
            ] + ([settings.BASE_URL + profile.get_absolute_url() + 'edit/?code=' + profile.verification_code] if with_url else []))
            num_alumni += 1
            if out != sys.stdout and num_alumni % 100 == 0:
                self.stdout.write(f'Export... {num_alumni} written.')
        if out != sys.stdout:
            out.close()
            self.stdout.write(f'Done. {num_alumni} written.')
