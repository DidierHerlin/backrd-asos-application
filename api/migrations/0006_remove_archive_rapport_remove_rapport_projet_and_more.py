# Generated by Django 4.2 on 2024-10-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_rapport_statut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='rapport',
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='projet',
        ),
        migrations.RemoveField(
            model_name='rapport',
            name='user',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.RemoveField(
            model_name='validation',
            name='rapport',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='contenu',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='date_notification',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='rapport',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='type',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('approved', 'Votre rapport a été bien approuvé'), ('rejected', 'Votre rapport a été rejeté')], default='approved', max_length=255),
        ),
        migrations.DeleteModel(
            name='Archive',
        ),
        migrations.DeleteModel(
            name='Projet',
        ),
        migrations.DeleteModel(
            name='Rapport',
        ),
        migrations.DeleteModel(
            name='Validation',
        ),
    ]