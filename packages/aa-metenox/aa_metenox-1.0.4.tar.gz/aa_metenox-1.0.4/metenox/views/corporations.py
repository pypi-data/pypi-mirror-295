"""Corporations views"""

from django_datatables_view.base_datatable_view import BaseDatatableView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from allianceauth.eveonline.evelinks import dotlan
from app_utils.views import link_html

from metenox.models import HoldingCorporation, Owner
from metenox.views.general import add_common_context

from ._helpers import corporation_notifications_button_html


@login_required
@permission_required("metenox.basic_access")
def list_corporations(request):
    """Will list all corporations and their statistics"""

    return render(request, "metenox/corporations.html", add_common_context())


# pylint: disable = too-many-ancestors
class CorporationListJson(
    PermissionRequiredMixin, LoginRequiredMixin, BaseDatatableView
):
    """Datatable view rendering corporations"""

    model = HoldingCorporation
    permission_required = "metenox.basic_access"
    columns = [
        "id",
        "corporation_name",
        "alliance_name",
        "count_metenoxes",
        "raw_revenue",
        "profit",
        "details",
    ]

    order_columns = [
        "pk",
        "",
        "",
        "",
        "",
        "",
        "",
    ]

    def render_column(self, row, column):
        if column == "id":
            return row.pk

        if column == "alliance_name":
            return self._render_alliance(row)

        if column == "corporation_name":
            return self._render_corporation(row)

        if column == "details":
            return self._render_details(row)

        return super().render_column(row, column)

    def _render_alliance(self, row: HoldingCorporation) -> str:
        alliance = row.corporation.alliance
        if alliance:
            alliance_link = link_html(
                dotlan.alliance_url(alliance.alliance_name), alliance.alliance_name
            )
            return alliance_link
        return ""

    def _render_corporation(self, row: HoldingCorporation) -> str:
        corporation_link = link_html(
            dotlan.corporation_url(row.corporation_name), row.corporation_name
        )
        return corporation_link

    def _render_details(self, row):
        return corporation_notifications_button_html(row)

    def get_initial_queryset(self):
        return self.initial_queryset(self.request)

    @classmethod
    def initial_queryset(cls, request):
        """Basic queryset of the function"""
        holding_corporations_query = HoldingCorporation.objects.select_related(
            "corporation",
            "corporation__alliance",
        ).filter(is_active=True)

        if not request.user.has_perm("metenox.auditor"):
            user_owners = Owner.objects.filter(character_ownership__user=request.user)
            holding_corporations_query = holding_corporations_query.filter(
                owners__in=user_owners
            )

        return holding_corporations_query

    def filter_queryset(self, qs):
        """Use params in the GET to filter"""

        qs = self._apply_search_filter(qs, 0, "corporation__corporation_name")

        qs = self._apply_search_filter(qs, 1, "corporation__alliance__alliance_name")

        return qs

    def _apply_search_filter(self, qs, column_num, field) -> models.QuerySet:
        my_filter = self.request.GET.get(f"columns[{column_num}][search][value]", None)
        if my_filter:
            if self.request.GET.get(f"columns[{column_num}][search][regex]", False):
                kwargs = {f"{field}__iregex": my_filter}
            else:
                kwargs = {f"{field}__istartswith": my_filter}
            return qs.filter(**kwargs)
        return qs


@login_required
@permission_required("metenox.basic_access")
def corporation_fdd_data(request) -> JsonResponse:
    """Provide lists for drop down fields"""
    qs = CorporationListJson.initial_queryset(request)
    columns = request.GET.get("columns")
    result = {}
    if columns:
        for column in columns.split(","):
            options = _calc_options(request, qs, column)
            result[column] = sorted(list(set(options)), key=str.casefold)
    return JsonResponse(result, safe=False)


# pylint: disable = too-many-return-statements, duplicate-code
def _calc_options(request, qs, column):
    if column == "alliance_name":
        values = qs.values_list("corporation__alliance__alliance_name", flat=True)
        values = (value for value in values if value)
        return values

    if column == "corporation_name":
        return qs.values_list("corporation__corporation_name", flat=True)

    return [f"** ERROR: Invalid column name '{column}' **"]


@login_required
@permission_required("metenox.basic_access")
def corporation_notifications(request, corporation_pk: int):
    """Render notification details of a corporation"""

    corporation = get_object_or_404(HoldingCorporation, pk=corporation_pk)
    context = {"corporation": corporation}

    if request.GET.get("new_page"):
        context["title"] = "Corporation notifications"
        context["content_file"] = "metenox/partials/corporation_notifications.html"
        return render(
            request,
            "metenox/modals/generic_modal_page.html",
            add_common_context(context),
        )

    return render(
        request,
        "metenox/modals/corporation_notifications.html",
        add_common_context(context),
    )
