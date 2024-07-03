# Generated by Django 5.0.6 on 2024-07-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yearbook', '0003_tag_student_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='students', to='yearbook.tag'),
        ),
    ]
