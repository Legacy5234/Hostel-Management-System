# Generated by Django 5.1.5 on 2025-01-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b_hostels', '0002_hostel_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostel',
            name='hostel_name',
            field=models.CharField(choices=[('New Boys', 'New Boys'), ('Old Boys', 'Old Boys'), ('Amazon', 'Amazon'), ('Serena', 'Serena')], max_length=100),
        ),
    ]
