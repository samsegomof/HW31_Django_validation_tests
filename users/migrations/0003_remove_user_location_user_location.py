# Generated by Django 4.1.3 on 2022-11-17 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.location', verbose_name='Местоположение'),
        ),
    ]