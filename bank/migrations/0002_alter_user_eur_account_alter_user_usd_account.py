# Generated by Django 5.1 on 2024-09-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='eur_account',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='usd_account',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
