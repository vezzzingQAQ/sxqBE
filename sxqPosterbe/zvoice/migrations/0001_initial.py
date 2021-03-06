# Generated by Django 3.2.5 on 2022-05-15 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('cid', models.BigIntegerField(default=0)),
                ('c_class', models.CharField(max_length=15)),
                ('c_class_id', models.IntegerField(default=0)),
                ('voice', models.IntegerField(default=0)),
                ('record', models.IntegerField(default=0)),
                ('visit_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
