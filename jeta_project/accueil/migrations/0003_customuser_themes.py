# Generated by Django 2.1.5 on 2019-02-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accueil', '0002_auto_20190227_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='themes',
            field=models.ManyToManyField(to='accueil.Theme'),
        ),
    ]
