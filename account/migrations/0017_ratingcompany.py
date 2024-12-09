# Generated by Django 5.1.2 on 2024-11-22 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_rating_suggested_number_of'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggested_number_of', models.IntegerField()),
                ('giver', models.CharField(max_length=255)),
                ('reciever', models.CharField(max_length=255)),
                ('rating_value', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
