# Generated by Django 5.1.5 on 2025-01-17 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupmember',
            old_name='is_banned',
            new_name='is_kicked',
        ),
    ]