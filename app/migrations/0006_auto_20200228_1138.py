# Generated by Django 2.2.4 on 2020-02-28 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200123_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursion',
            name='incharge',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_incharge', to='app.Incharge'),
        ),
    ]
