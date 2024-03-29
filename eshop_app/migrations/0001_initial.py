# Generated by Django 4.2.3 on 2023-07-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('available_quantity', models.IntegerField()),
            ],
        ),
    ]
