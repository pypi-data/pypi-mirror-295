# Generated by Django 2.2.13 on 2021-03-13 12:49

import NEMO.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import NEMO_billing.invoices.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rates", "0001_initial"),
        ("NEMO", "0028_version_3_9_0"),
    ]

    def create_invoice_customizations(apps, schema_editor):
        CustomizationModel = apps.get_model("NEMO", "Customization")
        CustomizationModel.objects.update_or_create(name="invoice_number_format", defaults={"value": "{:04d}"})
        CustomizationModel.objects.update_or_create(name="invoice_number_current", defaults={"value": "0"})

    operations = [
        migrations.CreateModel(
            name="InvoiceConfiguration",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "name",
                    models.CharField(help_text="The name of this invoice configuration", max_length=200, unique=True),
                ),
                (
                    "invoice_due_in",
                    models.PositiveIntegerField(
                        default=30, help_text="The default number of days invoices are due after"
                    ),
                ),
                (
                    "reminder_frequency",
                    models.PositiveIntegerField(
                        null=True,
                        blank=True,
                        default=7,
                        help_text="How often to send a reminder. Default value is 7, meaning every week after past due invoice",
                    ),
                ),
                ("email_from", models.EmailField(help_text="The email address used to send invoices and reminders")),
                (
                    "email_cc",
                    NEMO.fields.MultiEmailField(
                        null=True,
                        blank=True,
                        help_text="Email to cc the invoice to. A comma-separated list can be used",
                        max_length=2000,
                    ),
                ),
                (
                    "terms",
                    models.TextField(
                        null=True, blank=True, help_text="Terms and conditions to be included in the invoice"
                    ),
                ),
                ("merchant_name", models.CharField(max_length=255)),
                (
                    "merchant_details",
                    models.TextField(
                        blank=True,
                        help_text="The merchant details to be included in the invoice (address, phone number etc.)",
                        null=True,
                    ),
                ),
                (
                    "merchant_logo",
                    models.ImageField(
                        blank=True, null=True, upload_to=NEMO_billing.invoices.utilities.get_merchant_logo_filename
                    ),
                ),
                ("currency", models.CharField(default="USD", max_length=4)),
                ("currency_symbol", models.CharField(null=True, blank=True, max_length=4, default="$")),
                (
                    "tax",
                    models.DecimalField(
                        null=True,
                        blank=True,
                        decimal_places=3,
                        max_digits=5,
                        help_text="Tax in percent. For 20.5% enter 20.5",
                    ),
                ),
                ("tax_name", models.CharField(max_length=50, null=True, blank=True, default="VAT")),
                (
                    "detailed_invoice",
                    models.BooleanField(
                        default=True, help_text="Check this box if customers should receive a detailed invoice."
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectBillingDetails",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "category",
                    models.ForeignKey(null=True, blank=True, on_delete=models.SET_NULL, to="rates.RateCategory"),
                ),
                (
                    "project_name",
                    models.CharField(
                        blank=True,
                        help_text="The project name that will appear on the invoices. Leave blank to use NEMO project name",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "contact_name",
                    models.CharField(
                        blank=True, help_text="The contact name to use in the invoice email", max_length=255, null=True
                    ),
                ),
                (
                    "contact_email",
                    NEMO.fields.MultiEmailField(
                        null=True,
                        blank=True,
                        help_text="Email to send the invoice to. A comma-separated list can be used. Leave blank to use project managers/PIs emails",
                        max_length=2000,
                    ),
                ),
                (
                    "details",
                    models.TextField(
                        blank=True,
                        help_text="The project details to be included in the invoice (address, etc.)",
                        null=True,
                    ),
                ),
                (
                    "no_charge",
                    models.BooleanField(
                        default=False, help_text="Check this box if invoices should not be created for this project."
                    ),
                ),
                ("project", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to="NEMO.Project")),
            ],
            options={"verbose_name_plural": "Project details"},
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "invoice_number",
                    models.CharField(
                        blank=True, help_text="Leave blank to be assigned automatically", max_length=100, unique=True
                    ),
                ),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("due_date", models.DateField(null=True, blank=True)),
                ("sent_date", models.DateTimeField(null=True, blank=True)),
                ("last_sent_date", models.DateTimeField(null=True, blank=True)),
                ("last_reminder_sent_date", models.DateTimeField(null=True, blank=True)),
                ("reviewed_date", models.DateTimeField(null=True, blank=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("voided_date", models.DateTimeField(null=True, blank=True)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=14)),
                (
                    "configuration",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="invoices.InvoiceConfiguration"),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        null=True,
                        blank=True,
                        related_name="reviewed_invoice_set",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "voided_by",
                    models.ForeignKey(
                        null=True,
                        blank=True,
                        related_name="voided_invoice_set",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
                ),
                (
                    "file",
                    models.FileField(
                        null=True, blank=True, upload_to=NEMO_billing.invoices.utilities.get_invoice_document_filename
                    ),
                ),
                (
                    "project_details",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="invoices.ProjectBillingDetails"),
                ),
            ],
            options={
                "ordering": ["-created_date", "-invoice_number"],
            },
        ),
        migrations.CreateModel(
            name="InvoicePayment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("payment_received", models.DateField(help_text="Date when payment was received")),
                (
                    "payment_processed",
                    models.DateField(blank=True, help_text="Date when payment was processed", null=True),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14, help_text="Amount received")),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_created_by_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("invoice", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="invoices.Invoice")),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_updated_by_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-payment_received"],
            },
        ),
        migrations.CreateModel(
            name="InvoiceSummaryItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "summary_item_type",
                    models.IntegerField(
                        choices=[
                            (1, "item"),
                            (2, "category"),
                            (3, "small_category"),
                            (4, "sub_total"),
                            (5, "discount"),
                            (6, "facility_discount"),
                            (7, "tax"),
                            (8, "other"),
                        ]
                    ),
                ),
                ("core_facility", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(max_length=255)),
                ("details", models.CharField(blank=True, max_length=100, null=True)),
                ("amount", models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=14)),
                ("invoice", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="invoices.Invoice")),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceDetailItem",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("core_facility", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "item_type",
                    models.IntegerField(
                        choices=[
                            (1, "tool_usage"),
                            (2, "area_access"),
                            (3, "consumable"),
                            (4, "missed_reservation"),
                            (5, "staff_charge"),
                            (6, "training_session"),
                            (7, "custom_charge"),
                        ]
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=8)),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("user", models.CharField(max_length=200)),
                ("rate", models.CharField(blank=True, max_length=100, null=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=14)),
                ("invoice", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="invoices.Invoice")),
            ],
        ),
        migrations.RunPython(create_invoice_customizations),
    ]
