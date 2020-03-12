# Generated by Django 3.0.3 on 2020-03-12 06:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('uid', models.CharField(default=uuid.UUID('b789d4a4-8a9a-447a-90a5-e881fb1da6b7'), max_length=40)),
            ],
        ),
    ]