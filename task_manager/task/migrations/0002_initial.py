# Generated by Django 4.2.2 on 2023-07-26 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('label', '0001_initial'),
        ('status', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='author_tasks', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='executor_tasks', to=settings.AUTH_USER_MODEL, verbose_name='executor'),
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, through='task.Labeled', to='label.label', verbose_name='labels'),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, name='status', to='status.status', verbose_name='status'),
        ),
        migrations.AddField(
            model_name='labeled',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='label.label'),
        ),
        migrations.AddField(
            model_name='labeled',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
    ]
