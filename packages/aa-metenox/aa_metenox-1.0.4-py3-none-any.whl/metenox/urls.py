"""Routes."""

from django.urls import path

from . import views

app_name = "metenox"

urlpatterns = [
    path("", views.list_moons, name="index"),
    path("modal_loader_body", views.modal_loader_body, name="modal_loader_body"),
    path("moon/<int:moon_pk>", views.moon_details, name="moon_details"),
    path("moons_data", views.MoonListJson.as_view(), name="moons_data"),
    path("moons_fdd_data", views.moons_fdd_data, name="moons_fdd_data"),
    path("add_owner", views.add_owner, name="add_owner"),
    path("metenoxes", views.metenoxes, name="metenoxes"),
    path("metenoxes/<int:metenox_pk>", views.metenox_details, name="metenox_details"),
    path("metenoxes_data", views.MetenoxListJson.as_view(), name="metenoxes_data"),
    path("metenoxes_fdd_data", views.metenox_fdd_data, name="metenoxes_fdd_data"),
    path("corporations", views.list_corporations, name="corporations"),
    path(
        "corporations_data",
        views.CorporationListJson.as_view(),
        name="corporations_data",
    ),
    path(
        "corporations_fdd_data",
        views.corporation_fdd_data,
        name="corporations_fdd_data",
    ),
    path(
        "corporation/notification/<int:corporation_pk>",
        views.corporation_notifications,
        name="notifications",
    ),
    path("prices", views.prices, name="prices"),
]
