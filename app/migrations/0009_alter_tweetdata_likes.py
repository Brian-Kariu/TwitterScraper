# Generated by Django 4.0.5 on 2022-06-13 10:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_tweetdata_public_metrics_tweetdata_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetdata',
            name='likes',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
