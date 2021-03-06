# Generated by Django 3.1.13 on 2021-12-16 20:24

from django.db import migrations, models
from django.contrib.postgres.operations import  TrigramExtension


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brewery_id', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('cat_id', models.IntegerField()),
                ('style_id', models.IntegerField()),
                ('abv', models.FloatField()),
                ('ibu', models.FloatField()),
                ('srm', models.FloatField()),
                ('upc', models.IntegerField()),
                ('filepath', models.CharField(max_length=255)),
                ('descript', models.TextField()),
                ('add_user', models.IntegerField()),
                ('last_mod', models.TextField()),
            ],
            options={
                'db_table': 'beers',
            },
        ),
    ]
