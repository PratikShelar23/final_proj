# Generated by Django 4.2.4 on 2024-04-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0003_facultylogin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbsentNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
