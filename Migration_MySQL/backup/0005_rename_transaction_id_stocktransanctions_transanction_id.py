# Generated by Django 5.0.2 on 2024-04-01 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimplyWealthApp', '0004_stocktransanctions_userstockportfolio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocktransanctions',
            old_name='transaction_id',
            new_name='transanction_id',
        ),
    ]