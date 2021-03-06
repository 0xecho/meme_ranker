# Generated by Django 3.0.3 on 2021-05-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('about', models.CharField(max_length=500)),
                ('profile_picture', models.ImageField(upload_to='profile_pictures/')),
                ('show_telegram_username', models.BooleanField(default=False)),
                ('telegram_id', models.CharField(max_length=100)),
                ('telegram_username', models.CharField(max_length=100)),
                ('telegram_name', models.CharField(max_length=100)),
            ],
        ),
    ]
