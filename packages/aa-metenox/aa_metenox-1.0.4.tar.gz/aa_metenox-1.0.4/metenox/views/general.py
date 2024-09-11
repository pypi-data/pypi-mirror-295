"""Utility views or functions used everywhere"""

from django.shortcuts import render
from django.views.decorators.cache import cache_page

from metenox.models import Moon


def add_common_context(context: dict = None) -> dict:
    """Enhance the templates context with context that should be added to every page"""
    if context is None:
        context = {}

    if basic_title := context.get("page_title"):
        context["page_title"] = f"{basic_title} - Metenox"
    else:
        context["page_title"] = "Metenox"

    context["monthly_fuel_price"] = Moon.fuel_price()

    return context


@cache_page(3600)
def modal_loader_body(request):
    """Draw the loader body. Useful for showing a spinner while loading a modal."""
    return render(request, "metenox/modals/loader_body.html")
