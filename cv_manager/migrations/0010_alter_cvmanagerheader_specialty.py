# Generated by Django 4.2.1 on 2023-06-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_manager', '0009_cvmanagerheader_profile_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvmanagerheader',
            name='specialty',
            field=models.CharField(default='', max_length=100),
        ),
    ]