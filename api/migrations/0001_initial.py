# Generated by Django 4.2 on 2024-09-27 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lien_archive', models.URLField()),
                ('date_archive', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('contenu', models.TextField()),
                ('date_notification', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Projet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_projet', models.CharField(max_length=100, unique=True, verbose_name='Nom du Projet')),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('contenue', models.FileField(upload_to='rapports/')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(default='en attente', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField()),
                ('statu_validation', models.CharField(max_length=50)),
                ('rapport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rapport')),
            ],
        ),
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['title'], name='title_idx'),
        ),
        migrations.AddField(
            model_name='rapport',
            name='projet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.projet'),
        ),
        migrations.AddField(
            model_name='rapport',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='projet',
            constraint=models.UniqueConstraint(fields=('nom_projet',), name='unique_nom_projet'),
        ),
        migrations.AddField(
            model_name='notification',
            name='rapport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rapport'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='archive',
            name='rapport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.rapport'),
        ),
    ]
