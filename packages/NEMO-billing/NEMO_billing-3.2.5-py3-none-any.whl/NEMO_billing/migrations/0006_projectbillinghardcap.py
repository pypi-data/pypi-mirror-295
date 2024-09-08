# Generated by Django 4.2.11 on 2024-08-20 16:06

import re

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0012_invoiceconfiguration_invoice_title"),
        ("NEMO", "0086_adjustmentrequest_new_quantity"),
        ("NEMO_billing", "0005_version_2_5_6"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectBillingHardCap",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("enabled", models.BooleanField(default=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    "charge_types",
                    models.CharField(
                        help_text="List of charge types that will count towards this CAP",
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                re.compile("^\\d+(?:,\\d+)*\\Z"),
                                code="invalid",
                                message="Enter only digits separated by commas.",
                            )
                        ],
                    ),
                ),
                (
                    "configuration",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.invoiceconfiguration",
                    ),
                ),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="NEMO.project")),
            ],
            options={
                "ordering": ["-start_date"],
            },
        ),
    ]
