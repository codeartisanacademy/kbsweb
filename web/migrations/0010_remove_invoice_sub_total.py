# Generated by Django 3.2 on 2021-05-02 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_invoice_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='sub_total',
        ),
    ]
