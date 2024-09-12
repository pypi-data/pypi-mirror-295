"""
Utilities, split out for easier testing & mocking.
"""

from django.conf import settings


def get_course_from_modulestore(course_id):
    """
    Get course from modulestore.
    For whatever reason, this has to be a runtime import or it breaks a bunch
    of things.
    """
    # pylint: disable=import-outside-toplevel
    from xmodule.modulestore.django import modulestore

    return modulestore().get_course(course_id)


def get_configured_translation_languages():
    """
    Get configured languages for AI translation from settings.

    Returns:
    - List of{ "code": ISO language code, "label": Human readable language name }
    """
    return [
        {"code": code, "label": label}
        for code, label in settings.AI_TRANSLATIONS_LANGUAGE_CONFIG.items()
    ]
