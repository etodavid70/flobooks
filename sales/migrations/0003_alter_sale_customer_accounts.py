# Generated by Django 5.0.4 on 2024-07-30 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_alter_sale_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_account', models.JSONField()),
                ('bank_account', models.JSONField()),
                ('sales_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
        ),
    ]
