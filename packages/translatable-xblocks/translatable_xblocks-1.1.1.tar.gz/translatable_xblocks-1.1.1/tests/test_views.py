"""
Tests of api/views.py.
"""

from unittest.mock import patch

from ddt import ddt
from django.urls import reverse
from opaque_keys.edx.keys import CourseKey
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase


@ddt
class TestConfigApiGet(APITestCase):
    """Tests for ConfigApi GET endpoint."""

    valid_course_key = "course-v1:edX+DemoX+Demo_Course"
    configured_languages = [
        {"code": "en", "label": "English"},
        {"code": "gf", "label": "Gallifreyan"},
    ]

    def get_config_request(self, course_id):
        """Wraps the client call for ease of use."""
        return self.client.get(
            reverse("translatable-xblocks-config"), {"course_id": course_id}
        )

    @patch("translatable_xblocks.api.views.Config")
    def test_get_config(
        self,
        mock_config,
    ):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a valid course & settings
            course_id = self.valid_course_key

            mock_available = "foo"
            mock_enabled = "bar"

            mock_config.xpert_translations_available_for_course.return_value = (
                mock_available
            )
            mock_config.xpert_translations_enabled_for_course.return_value = (
                mock_enabled
            )

            # When I ask for the config
            response = self.get_config_request(course_id)

            # Then the response returns successfully...
            self.assertEqual(response.status_code, HTTP_200_OK)

            # ... with the expected data
            self.assertEqual(
                response.data["available_translation_languages"],
                self.configured_languages,
            )
            self.assertEqual(response.data["feature_available"], mock_available)
            self.assertEqual(response.data["feature_enabled"], mock_enabled)

    def test_get_config_missing_course_id(self):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a missing course_id
            # When I ask for the config
            response = self.client.get(reverse("translatable-xblocks-config"))

            # Then I get a 400 error
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_config_bad_course_id(self):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a missing course_id
            course_id = "blarg"

            # When I ask for the config
            response = self.get_config_request(course_id)

            # Then I get a 400 error
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_config_unauthenticated(self):
        # Given I'm not authenticated
        with patch.object(IsAuthenticated, "has_permission", return_value=False):
            course_id = self.valid_course_key

            # When I ask for the config
            response = self.get_config_request(course_id)

            # Then I get a 403 error
            self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


@ddt
class TestConfigApiSet(APITestCase):
    """Tests for ConfigApi POST endpoint."""

    valid_course_key = "course-v1:edX+DemoX+Demo_Course"

    def set_config_request(self, course_id, feature_enabled):
        """Wraps the client call for ease of use."""
        request_data = {"course_id": course_id, "feature_enabled": feature_enabled}
        return self.client.post(
            reverse("translatable-xblocks-config"), request_data, format="json"
        )

    @patch("translatable_xblocks.api.views.get_user_role")
    @patch("translatable_xblocks.api.views.Config.enable_xpert_translations_for_course")
    @patch("translatable_xblocks.api.views.Config")
    def test_set_config(
        self, mock_config, mock_set_feature_enabled, mock_get_user_role
    ):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a valid course & settings
            course_id = self.valid_course_key

            mock_config.xpert_translations_available_for_course.return_value = "foo"
            mock_config.xpert_translations_enabled_for_course.return_value = "bar"

            # When I, as staff, try to set the config
            mock_get_user_role.return_value = "staff"
            new_setting_value = "baz"

            response = self.set_config_request(course_id, new_setting_value)

            # Then the response returns successfully...
            self.assertEqual(response.status_code, HTTP_201_CREATED)

            # ... calling the right utility function
            mock_set_feature_enabled.assert_called_with(
                CourseKey.from_string(course_id), new_setting_value
            )

    def test_get_config_missing_course_id(self):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a missing course_id
            # When I ask for the config
            response = self.client.post(
                reverse("translatable-xblocks-config"), {"feature_enabled": True}
            )

            # Then I get a 400 error
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_config_bad_course_id(self):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a missing course_id
            course_id = "blarg"

            # When I ask for the config
            response = self.set_config_request(course_id, True)

            # Then I get a 400 error
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_config_missing_feature_enabled(self):
        with patch.object(IsAuthenticated, "has_permission", return_value=True):
            # Given a missing enabled flag
            course_id = self.valid_course_key

            # When I ask for the config
            response = self.client.post(
                reverse("translatable-xblocks-config"), {"course_id": course_id}
            )

            # Then I get a 400 error
            self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_get_config_unauthenticated(self):
        # Given I'm not authenticated
        with patch.object(IsAuthenticated, "has_permission", return_value=False):
            course_id = self.valid_course_key

            # When I ask for the config
            response = self.set_config_request(course_id, True)

            # Then I get a 403 error
            self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
