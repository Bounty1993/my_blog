# Generated by Django 2.2.1 on 2019-05-19 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]