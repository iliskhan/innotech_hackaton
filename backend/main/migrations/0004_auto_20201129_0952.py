# Generated by Django 3.1.3 on 2020-11-29 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201129_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkuserdata',
            name='interests',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vkuserpersonal',
            name='inspired_by',
            field=models.TextField(blank=True, null=True),
        ),
    ]
