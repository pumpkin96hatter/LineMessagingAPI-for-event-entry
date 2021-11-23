# Generated by Django 3.2.9 on 2021-11-22 14:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20211121_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application_info',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='application_info',
            name='application_log',
        ),
        migrations.RemoveField(
            model_name='application_info',
            name='entry',
        ),
        migrations.RemoveField(
            model_name='application_log',
            name='applied_at',
        ),
        migrations.RemoveField(
            model_name='application_log',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='application_log',
            name='status',
        ),
        migrations.AddField(
            model_name='application_info',
            name='applied_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='application_info',
            name='participant',
            field=models.CharField(default=9696, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application_info',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='application_log',
            name='amount',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application_log',
            name='application_info',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='events.application_info'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application_log',
            name='entry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.entry'),
        ),
    ]