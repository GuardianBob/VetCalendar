# Generated by Django 4.2.7 on 2024-01-11 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_alter_formoptions_option_label_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occupation',
            old_name='name',
            new_name='occupation',
        ),
    ]