# Generated by Django 5.0.4 on 2024-10-08 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0006_accountsreceivable"),
    ]

    operations = [
        migrations.RenameField(
            model_name="accountsreceivable",
            old_name="amount_due",
            new_name="amount",
        ),
        migrations.RemoveField(
            model_name="accountsreceivable",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="accountsreceivable",
            name="customer_name",
        ),
        migrations.RemoveField(
            model_name="accountsreceivable",
            name="due_date",
        ),
    ]