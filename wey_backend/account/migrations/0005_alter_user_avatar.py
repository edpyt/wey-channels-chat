# Generated by Django 4.2.1 on 2023-05-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_posts_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='300.jpg', null=True, upload_to='avatars'),
        ),
    ]