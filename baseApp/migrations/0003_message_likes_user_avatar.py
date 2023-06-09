# Generated by Django 4.2.1 on 2023-06-10 12:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='likes',
            field=models.ManyToManyField(related_name='message_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(default='avatar.svg', upload_to='chatBuddy_image_storage'),
        ),
    ]
