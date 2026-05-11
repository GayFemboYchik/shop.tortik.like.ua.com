from django.apps import AppConfig


class InstrumentShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instrument_shop'

    def ready(self):
        import instrument_shop.signals  # Обов'язково імпортуємо сигнали тут