# Generated by Django 3.0.4 on 2020-05-21 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('APIlend', '0004_auto_20200520_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='toAssign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignProposition', to='APIlend.UserProfile'),
        ),
    ]
