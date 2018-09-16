# Generated by Django 2.1 on 2018-09-08 00:10

from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.fields import ArrayField


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Surah',
            fields=[
                ('id', models.AutoField(
                    primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('total_ayahs', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ayah',
            fields=[
                ('id', models.AutoField(
                    primary_key=True,
                    serialize=False)),
                ('ayah', models.PositiveIntegerField(default=0)),
                ('text', ArrayField(
                    models.CharField(max_length=255, blank=True),
                    blank=True,
                    null=True)),
                ('surah', models.ForeignKey(
                    'Surah',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ayahs')),
            ],
        ),
    ]