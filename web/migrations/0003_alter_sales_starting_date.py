# Generated by Django 3.2 on 2021-04-28 17:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_sales_starting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='starting_date',
            field=models.DateField(default=datetime.date(2021, 4, 28), verbose_name='Mulai Kerja'),
            preserve_default=False,
        ),
    ]
