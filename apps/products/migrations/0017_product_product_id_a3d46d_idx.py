# Generated by Django 4.1.7 on 2023-04-26 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0016_region_alter_district_region"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["id"], name="product_id_a3d46d_idx"),
        ),
    ]