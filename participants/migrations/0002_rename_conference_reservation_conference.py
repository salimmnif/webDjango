# Generated by Django 4.2 on 2024-10-17 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='Conference',
            new_name='conference',
        ),
    ]