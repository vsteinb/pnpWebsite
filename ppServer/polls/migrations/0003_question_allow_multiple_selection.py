# Generated by Django 3.1.7 on 2022-08-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_show_result_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='allow_multiple_selection',
            field=models.BooleanField(default=False),
        ),
    ]
