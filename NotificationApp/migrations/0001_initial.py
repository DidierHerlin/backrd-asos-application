# Generated by Django 4.2 on 2024-10-02 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenue_notification', models.CharField(max_length=255)),
                ('message', models.CharField(choices=[('approved', 'Votre rapport a été bien approuvé'), ('rejected', 'Votre rapport a été rejeté'), ('En attente', 'votre rapport est en cours de validation')], default='En attente', max_length=255)),
            ],
        ),
    ]