# Generated by Django 3.2 on 2021-04-07 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210330_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
