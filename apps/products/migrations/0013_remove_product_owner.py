# Generated by Django 4.0.5 on 2023-04-05 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_productimage_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='owner',
        ),
    ]