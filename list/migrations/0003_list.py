# Generated by Django 3.1.3 on 2021-10-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0002_item_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
