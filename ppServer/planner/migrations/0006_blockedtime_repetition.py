# Generated by Django 3.2.16 on 2022-11-16 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0005_auto_20221116_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('start', models.DateTimeField(unique=True)),
                ('end', models.DateTimeField(unique=True)),
            ],
            options={
                'verbose_name': 'Blockierter Zeitraum',
                'verbose_name_plural': 'Blockierte Zeiträume',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='Repetition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField()),
                ('blocked_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planner.blockedtime')),
                ('interval', models.ManyToManyField(to='planner.Weekday')),
            ],
            options={
                'verbose_name': 'Wiederholung',
                'verbose_name_plural': 'Wiederholungen',
                'ordering': ['end_date'],
            },
        ),
    ]
