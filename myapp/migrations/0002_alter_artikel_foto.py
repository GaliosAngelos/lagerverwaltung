# Generated by Django 5.1.4 on 2024-12-26 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d'),
        ),
    ]