# Generated by Django 5.1.2 on 2024-11-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_job_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='education',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
