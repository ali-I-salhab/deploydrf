# Generated by Django 5.0.3 on 2024-03-29 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
