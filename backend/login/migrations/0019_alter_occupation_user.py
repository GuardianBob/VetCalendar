# Generated by Django 4.2.7 on 2024-01-11 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_alter_occupation_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_occupation', to='login.user'),
        ),
    ]