# Generated by Django 3.0.7 on 2021-06-28 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20210628_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='add_category',
            field=models.TextField(default='novel', max_length=100, verbose_name='add_Cat'),
        ),
    ]