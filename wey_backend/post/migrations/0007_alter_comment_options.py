# Generated by Django 4.2 on 2023-05-11 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',)},
        ),
    ]
