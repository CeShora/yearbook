# Generated by Django 5.0.6 on 2024-07-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yearbook', '0005_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
