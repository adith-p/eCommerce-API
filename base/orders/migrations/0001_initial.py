# Generated by Django 4.2.7 on 2023-11-20 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0002_product_model_pr_stock"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0005_delete_orders"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "order_id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("order_payment_id", models.CharField(blank=True, max_length=100)),
                ("order_price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processed", "Processed"),
                            ("ordered", "Ordered"),
                            ("shipped", "Shipped"),
                            ("delivery", "Delivery"),
                            ("cancel", "Cancel"),
                        ],
                        default="ordered",
                        max_length=100,
                    ),
                ),
                (
                    "MOP",
                    models.CharField(
                        choices=[("cod", "COD"), ("card", "Card")], max_length=100
                    ),
                ),
                ("date_of_order", models.DateTimeField(auto_now_add=True)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.address"
                    ),
                ),
                (
                    "order_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_item",
                        to="product.product_model",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_user_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]