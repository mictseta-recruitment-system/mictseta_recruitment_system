# Generated by Django 4.2.11 on 2024-06-06 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0007_profile_is_verified_personalinformation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressinformation',
            name='street_address_line1',
            field=models.CharField(max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='addressinformation',
            name='street_address_line',
            field=models.CharField(default='', max_length=225),
            preserve_default=False,
        ),
    ]
