# Generated by Django 2.0.1 on 2018-01-09 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplify', '0002_auto_20180109_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='key',
            field=models.CharField(default='684_5c+cB0-~a_Fc/56BA.B.8F~+BB7b', max_length=32, unique=True, validators=[django.core.validators.MaxLengthValidator(32), django.core.validators.MinLengthValidator(10)], verbose_name='Authentication key'),
        ),
    ]
