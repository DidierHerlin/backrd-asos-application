# Generated by Django 4.2 on 2024-10-02 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProjetApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('contenue', models.FileField(upload_to='rapports/')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('statut', models.PositiveSmallIntegerField(choices=[(0, 'Rejeté'), (1, 'Validé'), (2, 'En attente')], default=2)),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProjetApp.projet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]