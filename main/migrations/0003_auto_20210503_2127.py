# Generated by Django 3.1 on 2021-05-03 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
    ]
