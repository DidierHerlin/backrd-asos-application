# Generated by Django 4.2 on 2024-10-02 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_archive_rapport_remove_rapport_projet_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
