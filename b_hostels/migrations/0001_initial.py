# Generated by Django 5.1.5 on 2025-01-23 10:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostel_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='complaint_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='b_hostels.complaint')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10, null=True)),
                ('capacity', models.IntegerField(default=2)),
                ('occupants', models.IntegerField(default=0)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='b_hostels.hostel')),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='b_hostels.room'),
        ),
    ]
