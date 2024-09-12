"""
Translatable version of edx-platform/xmodule.html_block
"""

# pylint:  disable=unnecessary-lambda-assignment

from xblock.fields import Scope
from xmodule.html_block import HtmlBlock as OverriddenHtmlBlock

from translatable_xblocks.base import TranslatableXBlock
from translatable_xblocks.fields import TranslatableString

# Make '_' a no-op so we can scrape strings. Using lambda instead of
#  `django.utils.translation.gettext_noop` because Django cannot be imported in this file
_ = lambda text: text


class HtmlBlock(TranslatableXBlock, OverriddenHtmlBlock):
    """
    Translatable version of the HtmlBlock.

    Here, we only have to translate the data field.
    """

    data = TranslatableString(
        help=_("Html contents to display for this block"),
        default="",
        scope=Scope.content,
    )
