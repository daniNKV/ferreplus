from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_trade, name="trades_home"),
    path(
        "initiate/<int:requested_item_id>/",
        views.select_item_to_offer,
        name="propose_trade",
    ),
    path(
        "date-selection/<int:requested_item_id>/",
        views.select_possible_dates,
        name="dates_selection",
    ),
    path(
        "create/<int:requested_item_id>/<int:offered_item_id>/",
        views.make_proposal,
        name="create_proposal",
    ),
    path(
        "date-confirmation/<int:proposal_id>",
        views.accept_proposal,
        name="confirm_date",
    ),
    path("accept/<int:proposal_id>", views.accept_proposal, name="accept_proposal"),
    path(
        "counteroffer/<int:proposal_id>",
        views.counteroffer_proposal,
        name="counteroffer_proposal",
    ),
    path("decline/<int:proposal_id>", views.decline_proposal, name="decline_proposal"),
    path("detail/<int:proposal_id>", views.detail_proposal, name="detail_proposal"),
    path("history", views.show_history, name="show_history"),
    path("history/concreted", views.show_concreted_history, name="concreted_history"),
    path("history/canceled", views.show_canceled_history, name="canceled_history"),
    path("history/declined", views.show_declined_history, name="declined_history"),
    path("history/expired", views.show_expired_history, name="expired_history"),
]
