# Generated by Django 5.1 on 2024-10-22 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiontype',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
