# Generated by Django 2.0.4 on 2018-07-15 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boyScouts', '0010_group_user_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='scout',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
