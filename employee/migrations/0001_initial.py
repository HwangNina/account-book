# Generated by Django 3.1.4 on 2020-12-03 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('account', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=300)),
                ('is_admin', models.BooleanField()),
            ],
            options={
                'db_table': 'employees',
            },
        ),
    ]
