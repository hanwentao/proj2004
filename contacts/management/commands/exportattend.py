from collections import defaultdict

from django.core.management.base import BaseCommand

from ...models import Extra


class Command(BaseCommand):

    def handle(self, *args, **options):
        attend_counters = defaultdict(int)
        for extra in Extra.objects.filter(user__is_active=True):
            if not extra.attend:
                continue
            department_set = set()
            for class_ in extra.user.profile.classes.all():
                department_set.add(f'{class_.department.code} {class_.department.name}')
            for department in department_set:
                attend_counters[department] += 1
        for department, counter in sorted(attend_counters.items()):
            self.stdout.write(f'{department} {counter}')
