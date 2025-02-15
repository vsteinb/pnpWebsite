# Generated by Django 4.2.8 on 2024-10-30 16:28

from django.db import migrations


def fill_cost_values(apps, schema_editor):
    Priotable = apps.get_model('create', 'Priotable')

    rows = []
    for row in Priotable.objects.all().order_by("-priority"):
        row.cost = len(rows)+1
        rows.append(row)
    Priotable.objects.bulk_update(rows, ["cost"])


class Migration(migrations.Migration):

    dependencies = [
        ('create', '0037_priotable_cost'),
    ]

    operations = [
        migrations.RunPython(fill_cost_values),
    ]
