# Generated by Django 4.0.3 on 2022-07-10 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_order_ratings_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
    ]