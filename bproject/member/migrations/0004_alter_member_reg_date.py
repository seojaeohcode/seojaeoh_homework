# Generated by Django 4.1.1 on 2022-10-11 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_alter_member_reg_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='reg_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 11, 16, 9, 5, 882501)),
        ),
    ]
