# Generated by Django 3.1.3 on 2021-02-09 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_flight_count_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_swapped', models.DateField(auto_now_add=True)),
                ('owner', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='flight_count',
            name='date_swapped',
        ),
        migrations.RemoveField(
            model_name='flight_count',
            name='key',
        ),
    ]
