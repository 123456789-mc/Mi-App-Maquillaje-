# Generated by Django 3.2.8 on 2024-10-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0006_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='descripcion',
            field=models.CharField(blank=True, default='Descripción por defecto', max_length=250),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
