# Generated by Django 3.2 on 2022-04-30 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_alter_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.FloatField(default=1),
        ),
    ]
