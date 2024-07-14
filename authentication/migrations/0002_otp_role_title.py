# Generated by Django 5.0.6 on 2024-07-14 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=200)),
                ('code', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='title',
            field=models.CharField(choices=[('s', 'سهامدار'), ('c', 'مشتری'), ('e', 'کارمند')], default=0, max_length=1),
            preserve_default=False,
        ),
    ]