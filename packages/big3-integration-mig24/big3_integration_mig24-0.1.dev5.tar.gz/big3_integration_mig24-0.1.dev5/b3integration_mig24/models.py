from enum import Enum

from django.db import models
from integrations_market.models import AbstractSettingsSingleton


class SettingsMig24(AbstractSettingsSingleton):
    name_1 = models.CharField(max_length=1000, null=True, blank=True)
    name_2 = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return '<<App settings "b3integration_mig24">>'
