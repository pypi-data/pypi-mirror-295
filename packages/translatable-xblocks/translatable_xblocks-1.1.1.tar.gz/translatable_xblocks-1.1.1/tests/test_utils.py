"""Tests for translatable_xblocks/util.py"""

from unittest import TestCase
from unittest.mock import patch

import ddt
from lxml import etree

from translatable_xblocks.utils import (
    convert_html_to_xml,
    language_selection_to_django_language,
    language_selection_to_django_locale,
)


@ddt.ddt
class TestTranslationLanguageToDjangoLocale(TestCase):
    """Test for language_selection_to_django_local"""

    @ddt.unpack
    @ddt.data(
        ["en", "en"],
        ["ab-cd", "ab_CD"],  # Locale uses underscore and capitalized locale
    )
    def test_language_selection_to_django_locale(self, language_code, expected_locale):
        # Given a valid language code
        valid_language_code = language_code

        # When I ask for its correlated Django locale
        django_locale = language_selection_to_django_locale(valid_language_code)

        # Then I get the correct Django locale
        self.assertEqual(expected_locale, django_locale)

    @ddt.unpack
    @ddt.data(
        [
            "es",
            "es_419",
        ]  # Google only uses "es" for Spanish, but Django further differentiates by region
    )
    def test_language_selection_to_django_locale_special_cases(
        self, language_code, expected_locale
    ):
        # Given a language code that requires special mapping
        special_case_language_code = language_code

        # When I ask for its correlated Django locale
        django_locale = language_selection_to_django_locale(special_case_language_code)

        # Then I get the correct Django locale
        self.assertEqual(expected_locale, django_locale)

    @ddt.data(None, 323, object)
    def test_language_selection_to_django_locale_bad_arg(self, language_code):
        # Given a bad language code
        bad_language_code = language_code

        # When I ask for its correlated Django-locale
        django_locale = language_selection_to_django_locale(bad_language_code)

        # Then I return None
        self.assertIsNone(django_locale)


@ddt.ddt
class TestTranslationLanguageToDjangoLanguage(TestCase):
    """Tests for language_selection_to_django_language"""

    @ddt.unpack
    @ddt.data(
        ["en", "en"],
        ["ab-cd", "ab-cd"],  # Language uses hyphenated region selector
    )
    def test_language_selection_to_django_language(
        self, language_code, expected_django_language
    ):
        # Given a valid language code
        valid_language_code = language_code

        # When I ask for its correlated Django locale
        django_language = language_selection_to_django_language(valid_language_code)

        # Then I get the correct Django language code
        self.assertEqual(expected_django_language, django_language)

    @ddt.unpack
    @ddt.data(
        [
            "es",
            "es-419",
        ]  # Google only uses "es" for Spanish, but Django further differentiates by region
    )
    def test_language_selection_to_django_language_special_cases(
        self, language_code, expected_django_language
    ):
        # Given a language code that requires special mapping
        special_case_language_code = language_code

        # When I ask for its correlated Django locale
        django_language = language_selection_to_django_language(
            special_case_language_code
        )

        # Then I get the correct Django language code
        self.assertEqual(expected_django_language, django_language)

    @ddt.data(None, 323, object)
    def test_language_selection_to_django_language_bad_arg(self, language_code):
        # Given a bad language code
        bad_language_code = language_code

        # When I ask for its correlated Django-locale
        django_language = language_selection_to_django_language(bad_language_code)

        # Then I return None
        self.assertIsNone(django_language)


class TestHtmlXmlConversion(TestCase):
    """Tests for AiTranslationService."""

    @patch("translatable_xblocks.utils.get_platform_etree_lib")
    def test_convert_html_to_xml(self, mock_platform_etree):
        # edx-platform enforces its own import of etree for safety...
        # but for testing, we can just use etree
        mock_platform_etree.return_value = etree

        # Given an HTML response from the Google Translate API
        original_xml = '<option correct="False">Attributes should be quoted</option>'
        html_wrapped_xml = "<html><body><option correct=False>Attributes should be quoted</option></body></html>"

        # When I try to convert it to XML
        xml_output = convert_html_to_xml(html_wrapped_xml)

        # Then I get the expected output
        self.assertEqual(original_xml, xml_output)
