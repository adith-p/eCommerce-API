# Generated by Django 4.2.7 on 2023-11-19 10:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_wishlist_whishlist_item"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Orders",
        ),
    ]