# Generated by Django 4.2.1 on 2023-05-26 12:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0010_remove_postattachment_is_private_post_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reported_by_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
