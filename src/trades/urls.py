from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_trade, name="index"),
    path(
        "initiate/<int:requested_item_id>/", views.item_selection, name="propose_trade"
    ),
    path(
        "date-selection/<int:requested_item_id>/",
        views.dates_selection,
        name="dates_selection",
    ),
    path(
        "proposal-creation/<int:requested_item_id>/<int:offered_item_id>/",
        views.proposal_creation,
        name="proposal_creation",
    ),
]
