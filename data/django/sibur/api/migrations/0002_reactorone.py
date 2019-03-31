# Generated by Django 2.1.7 on 2019-03-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReactorOne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grate0_1', models.FloatField()),
                ('grate0_2', models.FloatField()),
                ('grate0_3', models.FloatField()),
                ('grate0_4', models.FloatField()),
                ('grate1_1', models.FloatField()),
                ('grate1_2', models.FloatField()),
                ('grate11_1', models.FloatField()),
                ('grate11_2', models.FloatField()),
                ('grate11_3', models.FloatField()),
                ('grate11_4', models.FloatField()),
                ('grate12_1', models.FloatField()),
                ('grate12_2', models.FloatField()),
                ('grate4_1', models.FloatField()),
                ('grate4_2', models.FloatField()),
                ('grate4_3', models.FloatField()),
                ('grate4_4', models.FloatField()),
                ('grate8_1', models.FloatField()),
                ('grate8_2', models.FloatField()),
                ('grate8_3', models.FloatField()),
                ('grate8_4', models.FloatField()),
                ('timestamp', models.DateField(blank=True)),
            ],
        ),
    ]