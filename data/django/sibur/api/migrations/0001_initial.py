# Generated by Django 2.1.7 on 2019-03-30 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
                ('role', models.CharField(max_length=1)),
            ],
        ),
    ]
