# Generated by Django 2.2.24 on 2021-07-30 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0004_version_1_6_0"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectbillingdetails",
            name="project",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="NEMO.Project"),
        ),
    ]
