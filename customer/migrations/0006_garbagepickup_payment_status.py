# Generated by Django 5.1.4 on 2025-03-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_garbagepickup_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='garbagepickup',
            name='payment_status',
            field=models.IntegerField(choices=[(0, 'Not Paid'), (1, 'Paid')], default=0),
        ),
    ]
