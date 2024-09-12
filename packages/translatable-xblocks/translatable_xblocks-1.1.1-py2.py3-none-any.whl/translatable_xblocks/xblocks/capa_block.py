"""
Translatable version of edx-platform/xmodule.capa_block
"""

# pylint:  disable=unnecessary-lambda-assignment

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from xblock.fields import Scope
from xmodule.capa_block import ProblemBlock as BaseProblemBlock

from translatable_xblocks.base import TranslatableXBlock
from translatable_xblocks.fields import TranslatableString, TranslatableXMLString

# Make '_' a no-op so we can scrape strings. Using lambda instead of
#  `django.utils.translation.gettext_noop` because Django cannot be imported in this file
_ = lambda text: text


try:
    FEATURES = getattr(settings, "FEATURES", {})
except ImproperlyConfigured:
    FEATURES = {}


class ProblemBlock(TranslatableXBlock, BaseProblemBlock):
    """Our version of the ProblemBlock with added translation logic."""

    display_name = TranslatableString(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        # it'd be nice to have a useful default but it screws up other things; so,
        # use display_name_with_default for those
        default=_("Blank Problem"),
    )

    data = TranslatableXMLString(
        help=_("XML data for the problem"),
        scope=Scope.content,
        enforce_type=FEATURES.get("ENABLE_XBLOCK_XML_VALIDATION", True),
        default="<problem></problem>",
    )

    def student_view(self, context, **kwargs):
        """
        Force answer message translation if should translate, then call parent rendering.
        """
        # Get translation source / destination language
        self.source_lang = context.get("src_lang")
        self.translate_lang = context.get("dest_lang")

        # CorrectMap is a map between answer_id and response evaluation result
        id_list = list(self.lcp.correct_map.keys())

        # If student has attempted the problem block
        if self.attempts > 0:
            # Get key from answer
            answer_id = id_list[0]

            # If translation behavior is enabled / selected...
            if self.should_translate:

                # Get answer message translated value
                translated_value = self.ai_translations_service.translate(
                    self.lcp.correct_map.get_msg(answer_id),
                    self.source_lang,
                    self.translate_lang,
                    self.location,
                    self.scope_ids.user_id,
                    cache_override=self.xt_cache_behavior,
                )

                # Update Correct Map message with translated result
                self.lcp.correct_map.set_property(answer_id, 'msg', translated_value)
            else:
                # Recalculate answer message as usual
                self.update_correctness()

        return super().student_view(context, **kwargs)
