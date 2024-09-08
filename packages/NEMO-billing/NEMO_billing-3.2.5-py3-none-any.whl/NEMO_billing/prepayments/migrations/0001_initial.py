# Generated by Django 3.2.19 on 2023-06-10 03:16

import re

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("NEMO", "0045_version_4_5_5"),
        ("NEMO_billing", "0004_version_2_4_0"),
    ]

    operations = [
        migrations.CreateModel(
            name="FundType",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="The unique name for this item", max_length=200, unique=True)),
                (
                    "display_order",
                    models.IntegerField(
                        help_text="The display order is used to sort these items. The lowest value category is displayed first."
                    ),
                ),
            ],
            options={
                "ordering": ["display_order", "name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProjectPrepaymentDetail",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "charge_types",
                    models.CharField(
                        help_text="List of charge types allowed",
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
                ("balance_last_updated", models.DateField(blank=True)),
                (
                    "only_core_facilities",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Limit which core facilities are allowed for this project. Leave blank to allow them all",
                        to="NEMO_billing.CoreFacility",
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
                (
                    "project",
                    models.OneToOneField(
                        help_text="The project",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="NEMO.project",
                        verbose_name="Project",
                    ),
                ),
            ],
            options={
                "ordering": ["project"],
            },
        ),
        migrations.CreateModel(
            name="Fund",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(blank=True, max_length=255, null=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    "start_month",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "JANUARY"),
                            (2, "FEBRUARY"),
                            (3, "MARCH"),
                            (4, "APRIL"),
                            (5, "MAY"),
                            (6, "JUNE"),
                            (7, "JULY"),
                            (8, "AUGUST"),
                            (9, "SEPTEMBER"),
                            (10, "OCTOBER"),
                            (11, "NOVEMBER"),
                            (12, "DECEMBER"),
                        ]
                    ),
                ),
                (
                    "start_year",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1900),
                            django.core.validators.MaxValueValidator(9999),
                        ]
                    ),
                ),
                (
                    "expiration_month",
                    models.PositiveIntegerField(
                        blank=True,
                        choices=[
                            (1, "JANUARY"),
                            (2, "FEBRUARY"),
                            (3, "MARCH"),
                            (4, "APRIL"),
                            (5, "MAY"),
                            (6, "JUNE"),
                            (7, "JULY"),
                            (8, "AUGUST"),
                            (9, "SEPTEMBER"),
                            (10, "OCTOBER"),
                            (11, "NOVEMBER"),
                            (12, "DECEMBER"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "expiration_year",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1900),
                            django.core.validators.MaxValueValidator(9999),
                        ],
                    ),
                ),
                ("balance", models.DecimalField(blank=True, decimal_places=2, max_digits=14)),
                (
                    "balance_warning_percent",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Send a warning email when the balance is below this percent.",
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                ("balance_warning_sent", models.DateTimeField(blank=True, null=True)),
                ("note", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "fund_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="prepayments.fundtype"),
                ),
                (
                    "project_prepayment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="prepayments.projectprepaymentdetail"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
