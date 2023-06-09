# Generated by Django 4.2.1 on 2023-06-11 04:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseApp', '0006_rename_save_message_savemsg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='message_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='saveMsg',
            field=models.ManyToManyField(blank=True, related_name='save_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='unLikes',
            field=models.ManyToManyField(blank=True, related_name='message_unLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
