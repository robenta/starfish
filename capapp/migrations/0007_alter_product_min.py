# Generated by Django 3.2.7 on 2021-10-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capapp', '0006_auto_20211008_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='min',
            field=models.IntegerField(default=1),
        ),
    ]