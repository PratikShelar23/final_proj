# Generated by Django 4.2.4 on 2024-04-03 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0011_remove_markatt_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='created_at',
        ),
    ]
