# Generated by Django 5.1.5 on 2025-01-17 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingmember',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetingmember', to='meeting.meeting'),
        ),
        migrations.AlterField(
            model_name='meetingmember',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetingmember', to='group.groupmember'),
        ),
        migrations.AddConstraint(
            model_name='meetingmember',
            constraint=models.UniqueConstraint(fields=('meeting', 'nickname'), name='unique_meeting_nickname'),
        ),
    ]
