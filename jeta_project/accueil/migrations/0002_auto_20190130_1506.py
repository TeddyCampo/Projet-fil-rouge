# Generated by Django 2.1.5 on 2019-01-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accueil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('top_score', models.IntegerField(default=0, verbose_name='high score')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
