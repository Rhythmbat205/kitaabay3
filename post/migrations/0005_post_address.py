# Generated by Django 3.0.7 on 2021-06-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20210623_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]