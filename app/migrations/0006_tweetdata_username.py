# Generated by Django 4.0.5 on 2022-06-10 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_tweetdata_tweet_id_alter_tweetdata_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetdata',
            name='username',
            field=models.CharField(default='elonmusk', max_length=255),
            preserve_default=False,
        ),
    ]
