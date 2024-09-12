"""
Views for the Translatable XBlocks API
"""

import logging

from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from translatable_xblocks.api.utils import get_configured_translation_languages
from translatable_xblocks.config import TranslatableXBlocksFeatureConfig as Config
from translatable_xblocks.platform_imports import get_user_role

logger = logging.getLogger(__name__)


class ConfigAPI(APIView):
    """Get / Set configuration for the translations feature."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        List feature configuration
        """

        # Lookup course from request
        course_id = request.GET.get("course_id")
        if not course_id:
            return HttpResponseBadRequest("course_id is required")
        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            return HttpResponseBadRequest(f"Invalid course course_id: {course_id}")

        # Check that feature is enabled
        feature_available = Config.xpert_translations_available_for_course(course_key)
        feature_enabled = Config.xpert_translations_enabled_for_course(course_key)

        # Get available translation languages
        available_translation_languages = get_configured_translation_languages()

        # Return Data
        return Response(
            {
                "available_translation_languages": available_translation_languages,
                "feature_available": feature_available,
                "feature_enabled": feature_enabled,
            }
        )

    def post(self, request):
        """
        Set feature configuration.
        """

        # Check correct POST body
        if "course_id" not in request.data:
            return HttpResponseBadRequest("course_id is required")
        if "feature_enabled" not in request.data:
            return HttpResponseBadRequest("feature_enabled is required")

        # Pull args from body
        course_id = request.data.get("course_id")
        feature_enabled = request.data.get("feature_enabled")

        # Validate course key
        try:
            course_key = CourseKey.from_string(course_id)
        except InvalidKeyError:
            return HttpResponseBadRequest(f"Invalid course course_id: {course_id}")

        # Check user has instructor / staff permissions
        if get_user_role(request.user, course_key) not in ("staff", "instructor"):
            return HttpResponseForbidden()

        # Set new feature value
        try:
            Config.enable_xpert_translations_for_course(course_key, feature_enabled)

        except ValueError:
            return Response(
                {
                    "available_translation_languages": get_configured_translation_languages(),
                    "feature_available": Config.xpert_translations_available_for_course(
                        course_key
                    ),
                    "feature_enabled": Config.xpert_translations_enabled_for_course(
                        course_key
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "available_translation_languages": get_configured_translation_languages(),
                "feature_available": Config.xpert_translations_available_for_course(
                    course_key
                ),
                "feature_enabled": Config.xpert_translations_enabled_for_course(
                    course_key
                ),
            },
            status=status.HTTP_201_CREATED,
        )
