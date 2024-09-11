import logging
import time

from b3platform.integrations_market.core import AbstractIntegrationCommand


class Command(AbstractIntegrationCommand):

    @property
    def integration_name(self) -> "str":
        return "mig24"

    @property
    def process_name(self) -> "str":
        return "get_raw_mchd"

    def get_logger(self) -> "logging.Logger":
        return logging.getLogger("b3")

    def handle(self, *args, **options) -> None:
        log = self.get_logger()
        log.info("Начало работы программы.")
        time.sleep(30)
        log.info("Завершение работы программы.")
