# Generated by Django 4.1.1 on 2022-10-11 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freeBoard', '0002_alter_fboard_b_date_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('r_no', models.AutoField(primary_key=True, serialize=False)),
                ('r_month', models.CharField(max_length=10)),
                ('r_revenue', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='c_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 11, 16, 9, 5, 884500)),
        ),
        migrations.AlterField(
            model_name='fboard',
            name='b_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 11, 16, 9, 5, 883500)),
        ),
    ]
