# Generated by Django 3.1.7 on 2022-04-12 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todays_fact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='fact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todays_fact.fact'),
        ),
    ]
