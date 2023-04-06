# Generated by Django 4.1.7 on 2023-04-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default=0, max_length=200)),
                ('message', models.TextField(default='', max_length=5000)),
            ],
        ),
    ]