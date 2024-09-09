"""Helpers for views."""

from moonmining.models import Moon

from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from app_utils.views import BootstrapStyle

from metenox.models import HoldingCorporation, Metenox


def generic_details_button_html(
    moon,
    django_detail_view,
    tooltip,
    detail_modal_id,
    fa_icon,
) -> str:
    """
    Return HTML to render a button that will call a modal with an object details.

    Rewriting the function `fontawesome_modal_button_html` from app_utils
    """

    ajax_url = reverse(django_detail_view, args=[moon.pk])

    return format_html(
        '<button type="button" '
        'class="btn btn-{}" '
        'data-bs-toggle="modal" '
        'data-bs-target="#{}" '
        "{}"
        "{}>"
        '<i class="{}"></i>'
        "</button>",
        BootstrapStyle(BootstrapStyle.DEFAULT),
        detail_modal_id,
        mark_safe(f'title="{tooltip}" ') if tooltip else "",
        mark_safe(f'data-ajax_url="{ajax_url}" ') if ajax_url else "",
        fa_icon,
    )


def moon_details_button_html(moon: Moon) -> str:
    """
    Return HTML to render a moon details button.

    Rewriting the function `fontawesome_modal_button_html` from app_utils
    """

    return generic_details_button_html(
        moon, "metenox:moon_details", "Moon details", "modalMoonDetails", "fas fa-moon"
    )


def metenox_details_button_html(metenox: Metenox) -> str:
    """
    Return an HTML button to display the modal with metenox details
    """

    return generic_details_button_html(
        metenox,
        "metenox:metenox_details",
        "Metenox details",
        "modalMetenoxDetails",
        "fas fa-moon",
    )


def corporation_notifications_button_html(holding: HoldingCorporation) -> str:
    """
    Returns an HTML button to display the modal with corporation notifications details
    """

    return generic_details_button_html(
        holding,
        "metenox:notifications",
        "Notification tool",
        "modalCorporationNotifications",
        "fas fa-bell",
    )
