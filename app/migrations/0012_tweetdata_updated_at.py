# Generated by Django 4.0.5 on 2022-06-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_tweetdata_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
