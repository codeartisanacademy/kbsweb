# Generated by Django 3.2 on 2021-05-11 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20210511_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryorder',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='delivery_orders', to='web.category'),
        ),
    ]
