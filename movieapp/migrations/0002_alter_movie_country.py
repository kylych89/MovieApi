# Generated by Django 4.0.4 on 2022-04-26 14:43

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
