# Generated by Django 5.0.6 on 2024-07-27 10:37

import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.CharField(max_length=100)),
                ('orderdate', models.DateField(max_length=50)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('phonenumber', models.BigIntegerField()),
                ('pincode', models.BigIntegerField()),
                ('orderstatus', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='media')),
                ('features', models.CharField(max_length=250)),
                ('category', models.CharField(max_length=50)),
                ('seller', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('status', models.CharField(default='pending', max_length=50)),
                ('rating', models.FloatField(default='3.5')),
                ('review', models.CharField(default='review', max_length=100)),
                ('additional_info', models.CharField(default='additional info', max_length=300)),
            ],
            options={
                'db_table': 'product',
            },
            managers=[
                ('productobj', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('usertype', models.CharField(max_length=50)),
                ('address_line1', models.CharField(max_length=50)),
                ('address_line2', models.CharField(default='area', max_length=50)),
                ('city', models.CharField(default='city', max_length=50)),
                ('state', models.CharField(default='state', max_length=50)),
                ('pincode', models.BigIntegerField()),
                ('contact', models.BigIntegerField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentmode', models.CharField(default='paypal', max_length=100)),
                ('paymentstatus', models.CharField(default='pending', max_length=100)),
                ('transaction_id', models.CharField(max_length=200)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.order')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.user')),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='Orderdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.CharField(max_length=100)),
                ('totalprice', models.IntegerField()),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.payment')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.user')),
            ],
            options={
                'db_table': 'orderdetail',
            },
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('totalamount', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myraingearapp.user')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
    ]
