# Generated by Django 4.1.3 on 2023-02-28 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='status',
            field=models.CharField(default=1, max_length=20, verbose_name='Status del pago'),
            preserve_default=False,
        ),
    ]