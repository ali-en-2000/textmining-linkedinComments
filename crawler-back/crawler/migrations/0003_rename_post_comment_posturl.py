# Generated by Django 4.1.7 on 2023-03-31 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_post_email_post_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='postUrl',
        ),
    ]
