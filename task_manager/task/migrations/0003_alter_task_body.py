# Generated by Django 4.2.2 on 2023-07-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='body',
            field=models.TextField(verbose_name='body'),
        ),
    ]