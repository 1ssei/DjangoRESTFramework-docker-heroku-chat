# Generated by Django 2.2.4 on 2019-11-13 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.User'),
            preserve_default=False,
        ),
    ]
