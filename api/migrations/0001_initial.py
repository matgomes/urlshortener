# Generated by Django 2.1.7 on 2019-04-10 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('original_url', models.URLField(db_column='OriginalUrl')),
                ('alias', models.CharField(db_column='Alias', max_length=15, unique=True)),
                ('hits', models.PositiveIntegerField(db_column='Hits', default=0)),
            ],
            options={
                'db_table': 'Url',
            },
        ),
    ]
