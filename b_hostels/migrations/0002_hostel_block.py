# Generated by Django 5.1.5 on 2025-01-23 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b_hostels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostel',
            name='block',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
