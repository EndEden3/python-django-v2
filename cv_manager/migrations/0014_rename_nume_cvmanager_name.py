# Generated by Django 4.2.1 on 2023-06-16 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cv_manager', '0013_cvmanager_nume_cvmanager_template_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cvmanager',
            old_name='nume',
            new_name='name',
        ),
    ]