# Generated by Django 4.1.1 on 2022-10-20 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_member_reg_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='reg_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 20, 17, 5, 40, 365584)),
        ),
    ]