# Generated by Django 4.2.4 on 2024-04-01 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0008_absentnote_user_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absentnote',
            name='user_details',
        ),
    ]
