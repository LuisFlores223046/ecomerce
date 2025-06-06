# Generated by Django 5.2 on 2025-04-23 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('roast_level', models.CharField(choices=[('light', 'Light Roast'), ('medium', 'Medium Roast'), ('dark', 'Dark Roast'), ('espresso', 'Espresso Roast')], max_length=20)),
                ('origin', models.CharField(max_length=100)),
                ('format', models.CharField(choices=[('whole_bean', 'Whole Bean'), ('ground', 'Ground'), ('capsule', 'Capsules')], max_length=20)),
                ('weight', models.IntegerField(help_text='Weight in grams')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_available', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
