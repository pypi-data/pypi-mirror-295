# Generated by Django 2.2.24 on 2021-09-02 17:42

from django.db import migrations, models

import NEMO_billing.invoices.utilities


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0005_version_1_6_1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="file",
            field=models.FileField(
                blank=True,
                max_length=255,
                null=True,
                upload_to=NEMO_billing.invoices.utilities.get_invoice_document_filename,
            ),
        ),
    ]
