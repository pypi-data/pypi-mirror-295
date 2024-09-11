from django.apps import AppConfig
from django.conf import settings

from . import app_settings as defaults

# Set some app default settings
for name in dir(defaults):
    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, getattr(defaults, name))


class NEMOBillingConfig(AppConfig):
    name = "NEMO_billing"
    verbose_name = "Billing"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        # Remove when NEMO 6.0.3 is released
        from NEMO.serializers import ModelSerializer
        from NEMO_billing.invoices.api import MultiEmailSerializerField
        from NEMO.fields import MultiEmailField

        ModelSerializer.serializer_field_mapping[MultiEmailField] = MultiEmailSerializerField
