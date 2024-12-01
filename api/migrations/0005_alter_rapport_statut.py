# Generated by Django 4.2 on 2024-09-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_rapport_est_accepte_alter_rapport_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapport',
            name='statut',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Rejeté'), (1, 'Validé'), (2, 'En attente')], default=2),
        ),
    ]
