# Generated by Django 5.1.5 on 2025-01-18 11:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_rename_is_banned_groupmember_is_kicked'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name='groupmember',
            index=models.Index(fields=['group', 'nickname'], name='group_group_group_i_cfe62f_idx'),
        ),
    ]
