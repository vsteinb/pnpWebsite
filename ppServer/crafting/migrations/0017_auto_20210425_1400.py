# Generated by Django 3.1.5 on 2021-04-25 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crafting', '0016_auto_20210408_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialdrop',
            name='item',
        ),
        migrations.RemoveField(
            model_name='materialdrop',
            name='material',
        ),
        migrations.DeleteModel(
            name='Material',
        ),
        migrations.DeleteModel(
            name='MaterialDrop',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]
