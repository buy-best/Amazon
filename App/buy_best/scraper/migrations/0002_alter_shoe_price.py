# Generated by Django 5.0.6 on 2024-07-11 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
