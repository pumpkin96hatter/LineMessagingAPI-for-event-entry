# Generated by Django 3.2.9 on 2022-01-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_event_type_pic_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suchedule_url', models.CharField(default='', max_length=300)),
            ],
        ),
    ]
