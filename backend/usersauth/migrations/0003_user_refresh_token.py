# Generated by Django 5.2.4 on 2025-07-21 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersauth', '0002_alter_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
