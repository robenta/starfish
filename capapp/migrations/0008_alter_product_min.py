# Generated by Django 3.2.7 on 2021-10-08 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capapp', '0007_alter_product_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min',
            field=models.IntegerField(default=100),
        ),
    ]