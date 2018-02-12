from django.db import migrations

def upgrade(apps, schema_editor):
    Department = apps.get_model('contacts', 'Department')
    Clazz = apps.get_model('contacts', 'Clazz')
    Profile = apps.get_model('contacts', 'Profile')
    for profile in Profile.objects.all():
        department_name = profile.department
        clazz_name = profile.clazz
        department, _ = Department.objects.get_or_create(name=department_name, defaults={
            'code': '000',
        })
        clazz, _ = Clazz.objects.get_or_create(name=clazz_name, defaults={
            'department': department,
        })
        profile.clazzes.add(clazz)

def downgrade(apps, schema_editor):
    Profile = apps.get_model('contacts', 'Profile')
    for profile in Profile.objects.all():
        department_name = profile.clazzes.first().department.name
        clazz_name = profile.clazzes.first().name
        profile.department = department_name
        profile.clazz = clazz_name
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0016_profile_clazzes'),
    ]

    operations = [
        migrations.RunPython(upgrade, downgrade),
    ]
