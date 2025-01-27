# Generated by Django 3.0 on 2019-12-04 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='name')),
                ('initials', models.CharField(blank=True, max_length=40, null=True, verbose_name='initials')),
            ],
            options={
                'db_table': 'geo_state',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True, verbose_name='name')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.State', verbose_name='state')),
            ],
            options={
                'db_table': 'geo_city',
            },
        ),
    ]
