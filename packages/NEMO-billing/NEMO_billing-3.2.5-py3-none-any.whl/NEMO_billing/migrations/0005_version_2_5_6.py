# Generated by Django 3.2.19 on 2023-06-26 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("NEMO_billing", "0004_version_2_4_0"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="institution",
            options={"ordering": ["name"]},
        ),
    ]
