# Generated by Django 4.2 on 2024-09-30 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projet',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='projet',
            name='unique_nom_projet',
        ),
        migrations.AlterField(
            model_name='projet',
            name='nom_projet',
            field=models.CharField(max_length=255),
        ),
    ]