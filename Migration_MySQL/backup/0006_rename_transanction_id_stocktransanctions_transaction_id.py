# Generated by Django 5.0.2 on 2024-04-01 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SimplyWealthApp', '0005_rename_transaction_id_stocktransanctions_transanction_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocktransanctions',
            old_name='transanction_id',
            new_name='transaction_id',
        ),
    ]
