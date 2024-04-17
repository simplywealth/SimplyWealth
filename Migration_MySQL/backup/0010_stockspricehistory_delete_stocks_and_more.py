# Generated by Django 5.0.4 on 2024-04-07 13:25

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SimplyWealthApp", "0009_leaderboard"),
    ]

    operations = [
        migrations.CreateModel(
            name="StocksPriceHistory",
            fields=[
                (
                    "unique_key",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("current_time", models.DateField(auto_now_add=True)),
                ("stock_name", models.CharField(max_length=10)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.DeleteModel(
            name="Stocks",
        ),
        migrations.RenameField(
            model_name="leaderboard",
            old_name="price",
            new_name="current_total",
        ),
        migrations.RemoveField(
            model_name="leaderboard",
            name="stock_name",
        ),
        migrations.AddField(
            model_name="leaderboard",
            name="userid",
            field=models.CharField(
                default=datetime.datetime(2024, 4, 7, 13, 25, 31, 597413), max_length=30
            ),
            preserve_default=False,
        ),
    ]
