# Generated by Django 4.2.7 on 2024-01-09 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_alter_userlevel_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesslevel',
            name='users',
            field=models.ManyToManyField(default=1, related_name='user_level', to='login.user'),
        ),
        migrations.DeleteModel(
            name='UserLevel',
        ),
    ]
