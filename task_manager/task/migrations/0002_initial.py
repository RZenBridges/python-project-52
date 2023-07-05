# Generated by Django 4.2.2 on 2023-06-19 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('label', '0001_initial'),
        ('task', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(through='task.Labeled', to='label.label'),
        ),
        migrations.AddField(
            model_name='task',
            name='performer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task_performer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task_status', to='status.status'),
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