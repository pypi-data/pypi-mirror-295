""" Common config across environments """


def plugin_settings(settings):
    """
    App-specific settings
    """

    # Available languages for translation
    settings.AI_TRANSLATIONS_LANGUAGE_CONFIG = {
        "en": "English",
        "es": "Español",
        "ar": "العربية",
    }

    # TTL in seconds for successful request to store in cache
    settings.REQUEST_CACHE_SUCCESS_TIMEOUT = 86400

    # TIL in seconds for failure request to store in cache
    settings.REQUEST_CACHE_FAILURE_TIMEOUT = 300
