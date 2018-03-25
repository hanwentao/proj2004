import csv
import sys

from django.core.management.base import BaseCommand

from ...models import Department


class Command(BaseCommand):
    help = 'Display statistics.'

    def handle(self, *args, **options):
        writer = csv.writer(sys.stdout)
        writer.writerow([
            '代码',
            '院系',
            '人数',
            '登录人数',
            '50%填写人数',
            '80%填写人数',
            '申请校友卡人数',
            '参加秩年活动人数',
            '不参加秩年活动人数',
            '申请校友邮箱人数',
        ])
        for department in Department.objects.all():
            alumni_set = set()
            counter = 0
            login_counter = 0
            p50_counter = 0
            p80_counter = 0
            card_counter = 0
            attend_counter = 0
            not_attend_counter = 0
            email_counter = 0
            for class_ in department.class_set.all():
                for profile in class_.profile_set.all():
                    user = profile.user
                    if not user.is_active:
                        continue
                    if profile.student_id in alumni_set:
                        continue
                    extra = user.extra
                    alumni_set.add(profile.student_id)
                    counter += 1
                    if user.last_login: login_counter += 1
                    if profile.completeness >= 0.5: p50_counter += 1
                    if profile.completeness >= 0.8: p80_counter += 1
                    if extra.photo: card_counter += 1
                    if extra.attend: attend_counter += 1
                    if extra.attend is False: not_attend_counter += 1
                    if extra.email_prefix: email_counter += 1
            writer.writerow([
                department.code,
                department.name,
                counter,
                login_counter,
                p50_counter,
                p80_counter,
                card_counter,
                attend_counter,
                not_attend_counter,
                email_counter,
            ])
