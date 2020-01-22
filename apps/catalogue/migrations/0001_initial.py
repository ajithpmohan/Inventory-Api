# Generated by Django 2.2.9 on 2020-01-22 14:59

import autoslug.fields
import django.core.validators
from django.conf import settings
from django.db import migrations, models

import apps.utils.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=True, populate_from='name', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=apps.utils.helpers.default_content_path, verbose_name='Image')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(help_text='A particular group of related products', on_delete='Category', related_name='products', related_query_name='product', to='catalogue.Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RequestedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Requested Stock')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Requested Date')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=1, verbose_name='Status')),
                ('summary', models.TextField(blank=True)),
                ('product', models.ForeignKey(help_text='The requested product.', on_delete='Requested Product', related_name='requesteditems', related_query_name='requested_item', to='catalogue.Product')),
                ('user', models.ForeignKey(help_text='The user who requested the product.', on_delete='Requested By', related_name='requesteditems', related_query_name='requested_item', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'RequestedItem',
                'verbose_name_plural': 'RequestedItems',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(verbose_name='Stock Quantity')),
                ('limit', models.PositiveSmallIntegerField(help_text='Admin get notification when stock quantity value is less than stock limit value.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Stock Limit')),
                ('product', models.OneToOneField(on_delete='Product', related_name='stock', related_query_name='stock', to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'ProductStock',
                'verbose_name_plural': 'ProductStocks',
                'ordering': ['product__name'],
            },
        ),
        migrations.CreateModel(
            name='IssuedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Issued Stock')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Issued Date')),
                ('summary', models.TextField(blank=True)),
                ('product', models.ForeignKey(help_text='The issued product.', on_delete='Issued Product', related_name='issueditems', related_query_name='issued_item', to='catalogue.Product')),
                ('user', models.ForeignKey(help_text='The user in which product is issued.', on_delete='Issued To', related_name='issueditems', related_query_name='issued_item', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'IssuedItem',
                'verbose_name_plural': 'IssuedItems',
                'ordering': ['-timestamp'],
            },
        ),
    ]