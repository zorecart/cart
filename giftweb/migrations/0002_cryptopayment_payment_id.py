# Generated by Django 4.2.7 on 2024-05-18 14:30

from django.db import migrations, models
import giftweb.models


class Migration(migrations.Migration):

    dependencies = [
        ('giftweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptopayment',
            name='payment_id',
            field=models.CharField(blank=True, default=giftweb.models.generate_tracking_id, max_length=100),
        ),
    ]
