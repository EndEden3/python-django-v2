# Generated by Django 4.2.1 on 2023-06-15 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_manager', '0008_cvmanagerskill'),
    ]

    operations = [
        migrations.AddField(
            model_name='cvmanagerheader',
            name='profile_details',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='cvmanagerheader',
            name='specialty',
            field=models.CharField(default='', max_length=10),
        ),
    ]