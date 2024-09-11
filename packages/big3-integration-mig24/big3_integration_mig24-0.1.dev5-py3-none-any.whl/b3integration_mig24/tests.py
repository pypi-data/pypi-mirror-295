from django.core.management import call_command
from django.test import TestCase

from data_exchange_with_external_systems.constants import TaskStatuses
from integrations_market.models import IntegrationProcessStatus


class TestIntegrationCommand(TestCase):

    def test_test_completed_command(self):
        self.assertFalse(IntegrationProcessStatus.objects.exists())
        call_command("get_raw_mchd")
        integration_process_status = IntegrationProcessStatus.objects.get()
        self.assertEqual(integration_process_status.status, TaskStatuses.COMPLETED.code)

    def test_test_error_command(self):
        self.assertFalse(IntegrationProcessStatus.objects.exists())
        call_command("get_raw_mchd")
        integration_process_status = IntegrationProcessStatus.objects.get()
        self.assertEqual(integration_process_status.status, TaskStatuses.COMPLETED.code)
