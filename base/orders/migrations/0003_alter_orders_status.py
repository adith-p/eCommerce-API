# Generated by Django 4.2.7 on 2023-11-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_orders_date_of_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="status",
            field=models.CharField(
                choices=[
                    ("processed", "Processed"),
                    ("ordered", "Ordered"),
                    ("shipped", "Shipped"),
                    ("delivery", "Delivery"),
                    ("cancel", "Cancel"),
                ],
                default="processed",
                max_length=100,
            ),
        ),
    ]
