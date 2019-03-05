# Generated by Django 2.1.7 on 2019-03-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access_token',
        ),
        migrations.AddField(
            model_name='user',
            name='access_code',
            field=models.CharField(default=1, max_length=300, verbose_name='Spotify API access code'),
            preserve_default=False,
        ),
    ]
