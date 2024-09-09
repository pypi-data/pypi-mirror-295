"""Admin site."""

from django.contrib import admin

from metenox.models import (
    EveTypePrice,
    HoldingCorporation,
    Metenox,
    MetenoxHourlyProducts,
    MetenoxStoredMoonMaterials,
    Moon,
    Owner,
)
from metenox.templatetags.metenox import formatisk


class MetenoxHourlyHarvestInline(admin.TabularInline):
    model = MetenoxHourlyProducts

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ["name", "moon_value", "value_updated_at"]
    fields = [("eve_moon", "moonmining_moon"), ("value", "value_updated_at")]
    search_fields = ["eve_moon__name"]
    readonly_fields = ["eve_moon", "moonmining_moon"]
    inlines = (MetenoxHourlyHarvestInline,)

    @admin.display(description="value")
    def moon_value(self, moon: Moon):
        return f"{formatisk(moon.value)} ISK"

    def has_add_permission(self, request):
        return False


class MetenoxMoonMaterialBayInline(admin.TabularInline):
    model = MetenoxStoredMoonMaterials

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Metenox)
class MetenoxAdmin(admin.ModelAdmin):
    list_display = [
        "structure_name",
        "corporation",
        "metenox_value",
        "fuel_blocks_count",
        "magmatic_gas_count",
    ]
    fields = [
        ("structure_id", "structure_name"),
        "moon",
        "corporation",
        ("fuel_blocks_count", "magmatic_gas_count"),
    ]
    readonly_fields = ["structure_id", "moon"]
    inlines = (MetenoxMoonMaterialBayInline,)

    @admin.display(description="value")
    def metenox_value(self, metenox: Metenox):
        return f"{formatisk(metenox.moon.value)} ISK"

    def has_add_permission(self, request):
        return False


class OwnerCharacterAdminInline(admin.TabularInline):
    model = Owner

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(HoldingCorporation)
class HoldingCorporationAdmin(admin.ModelAdmin):
    list_display = ["corporation", "is_active", "count_metenox"]
    readonly_fields = ["corporation", "last_updated", "count_metenox"]
    inlines = (OwnerCharacterAdminInline,)

    @admin.display(description="Number metenoxes")
    def count_metenox(self, holding: HoldingCorporation) -> int:
        return holding.count_metenoxes

    def has_add_permission(self, request):
        return False


@admin.register(EveTypePrice)
class EveTypePriceAdmin(admin.ModelAdmin):
    list_display = ["eve_type", "type_price"]
    readonly_fields = ["eve_type", "last_update"]

    @admin.display(description="Price")
    def type_price(self, type_price: EveTypePrice):
        return f"{formatisk(type_price.price)} ISK"

    def has_add_permission(self, request):
        return False
