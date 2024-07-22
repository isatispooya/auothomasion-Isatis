# Generated by Django 5.0.6 on 2024-07-21 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0005_letter_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='attachment',
            field=models.ManyToManyField(blank=True, null=True, related_name='attachment', to='letter.attachment'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='letter_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='letter',
            name='year',
            field=models.IntegerField(),
        ),
    ]