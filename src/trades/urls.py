from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_trade, name="trades_home"),
    path(
        "initiate/<int:requested_item_id>/", views.item_selection, name="propose_trade"
    ),
    path(
        "detail/<int:proposal_id>/", views.detail_proposal, name="detail_proposal"
    ),
    path(
        "date-selection/<int:requested_item_id>/",
        views.dates_selection,
        name="dates_selection",
    ),
    path(
        "create/<int:requested_item_id>/<int:offered_item_id>/",
        views.proposal_creation,
        name="create_proposal",
    ),
    path(
        "history",
        views.show_history,
        name="show_history"
    )
    #path("detail/<int:trade_id>", views.trade_detail, name="detail_trade"),
]
