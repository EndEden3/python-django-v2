# Generated by Django 4.2.1 on 2023-06-18 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cv_manager', '0015_alter_cvmanager_template_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cvmanager',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
