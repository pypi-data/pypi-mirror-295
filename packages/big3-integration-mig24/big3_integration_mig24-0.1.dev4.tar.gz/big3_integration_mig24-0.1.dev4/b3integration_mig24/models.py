from enum import Enum

from django.db import models
from integrations_market.models import AbstractSettingsSingleton


class SettingsMig24(AbstractSettingsSingleton):
    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return '<<App settings "b3integration_mig24">>'
