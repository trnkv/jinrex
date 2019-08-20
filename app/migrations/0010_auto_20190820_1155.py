# Generated by Django 2.2.4 on 2019-08-20 11:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_auto_20190820_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excursion',
            name='id_guide',
        ),
        migrations.RemoveField(
            model_name='excursion',
            name='name_organizator',
        ),
        migrations.AddField(
            model_name='excursion',
            name='guide',
            field=models.ForeignKey(default='', help_text='Select desired guide for this excursion', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_guide', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='excursion',
            name='incharge',
            field=models.ForeignKey(default='', editable=False, help_text='Responsible for the excursion', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_incharge', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='excursion',
            name='organizator',
            field=models.ForeignKey(default='', help_text='Enter the name of the excursion organizator', on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_organizator', to=settings.AUTH_USER_MODEL),
        ),
    ]
