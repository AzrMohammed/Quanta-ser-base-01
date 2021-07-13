# Generated by Django 2.2.6 on 2021-04-27 16:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GEN', '0043_auto_20210427_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandappspecificdetails',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brandappspecificdetails',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='brandappspecificdetails',
            name='is_online',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='brandappspecificdetails',
            name='status',
            field=models.CharField(choices=[('AT', 'ACTIVE'), ('IA', 'INACTIVE'), ('DS', 'DISABLED'), ('DL', 'DELETED')], default='AT', max_length=2),
        ),
        migrations.AddField(
            model_name='brandappspecificdetails',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]