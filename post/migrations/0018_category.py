# Generated by Django 3.0.7 on 2021-07-04 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20210704_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]