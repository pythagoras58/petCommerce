# Generated by Django 3.2.9 on 2021-11-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]