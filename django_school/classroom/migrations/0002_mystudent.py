# Generated by Django 2.0.1 on 2019-05-01 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateTimeField()),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=20)),
                ('contactnum', models.IntegerField()),
                ('egap', models.IntegerField()),
                ('tenper', models.IntegerField()),
                ('tenyop', models.IntegerField()),
                ('tweper', models.IntegerField()),
                ('tweyop', models.IntegerField()),
                ('regid', models.IntegerField()),
                ('rollno', models.CharField(max_length=20)),
                ('gper', models.IntegerField()),
                ('back', models.IntegerField()),
                ('branch', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'MyStudent',
            },
        ),
    ]
