# Generated by Django 4.0.6 on 2022-09-21 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('great', '0002_mypage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='great_id',
        ),
        migrations.AddField(
            model_name='picture',
            name='great_id',
            field=models.OneToOneField(db_column='great_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='great', to='great.great'),
        ),
    ]
