# Generated by Django 4.0.5 on 2022-06-14 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_tweetdata_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdata',
            name='created_at',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
    ]
