# Generated by Django 4.1.7 on 2023-08-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_space', '0010_auto_20220415_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('width', models.PositiveSmallIntegerField(default=15)),
                ('height', models.PositiveSmallIntegerField(default=6)),
                ('tiles', models.JSONField(default=list)),
            ],
            options={
                'verbose_name': 'Level',
                'verbose_name_plural': 'Levels',
                'ordering': ['name'],
            },
        ),
        migrations.DeleteModel(
            name='Aktivator',
        ),
        migrations.DeleteModel(
            name='Barriere',
        ),
        migrations.DeleteModel(
            name='Duplikator',
        ),
        migrations.DeleteModel(
            name='Inverter',
        ),
        migrations.DeleteModel(
            name='Konverter',
        ),
        migrations.DeleteModel(
            name='Linearriss',
        ),
        migrations.DeleteModel(
            name='Liniendeletion',
        ),
        migrations.DeleteModel(
            name='Looper',
        ),
        migrations.DeleteModel(
            name='Manabombe',
        ),
        migrations.DeleteModel(
            name='ManaDegenerator',
        ),
        migrations.RemoveField(
            model_name='metasplinter',
            name='splinter_ptr',
        ),
        migrations.DeleteModel(
            name='Mirror',
        ),
        migrations.DeleteModel(
            name='Net',
        ),
        migrations.DeleteModel(
            name='Runner',
        ),
        migrations.DeleteModel(
            name='Sensorgatter',
        ),
        migrations.DeleteModel(
            name='Supportgatter',
        ),
        migrations.DeleteModel(
            name='Switch',
        ),
        migrations.DeleteModel(
            name='Teleportgatter',
        ),
        migrations.DeleteModel(
            name='Timedelayer',
        ),
        migrations.DeleteModel(
            name='Timelagger',
        ),
        migrations.DeleteModel(
            name='Tracinggatter',
        ),
        migrations.DeleteModel(
            name='Metasplinter',
        ),
        migrations.DeleteModel(
            name='Splinter',
        ),
    ]
