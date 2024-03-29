# Generated by Django 4.0.3 on 2022-07-12 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_rate_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='occupied',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart',
            name='barcode',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='cartnumber',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='currentuser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserProfile', to=settings.AUTH_USER_MODEL),
        ),
    ]
