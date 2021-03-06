# Generated by Django 3.1.3 on 2021-05-30 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=2048)),
                ('club_picture', models.ImageField(blank=True, upload_to='club_uploads/')),
                ('admin', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='club_admin', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(blank=True, related_name='follows', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='club', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='member_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('club', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='announcements.club')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048)),
                ('details', models.CharField(max_length=2048)),
                ('date_time', models.DateTimeField()),
                ('open_to_all', models.BooleanField()),
                ('photo', models.ImageField(blank=True, upload_to='upload/')),
                ('interested', models.ManyToManyField(blank=True, related_name='interests', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.club')),
                ('participants', models.ManyToManyField(blank=True, related_name='event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=2048)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='announcements.event')),
            ],
        ),
    ]
