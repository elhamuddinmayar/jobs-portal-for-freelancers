# Generated by Django 5.1.2 on 2024-11-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_company_background_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education_background',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='interests',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='personal_skills',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_experience',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
