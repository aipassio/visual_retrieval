# Generated by Django 3.1.6 on 2021-02-16 06:59

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('object_img', models.CharField(max_length=900000)),
                ('features', jsonfield.fields.JSONField()),
            ],
        ),
    ]