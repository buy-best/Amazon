# Generated by Django 5.0.6 on 2024-07-20 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report', '0001_initial'),
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='tracker.product'),
        ),
    ]