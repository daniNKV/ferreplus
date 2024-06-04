from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("employee/", views.employee_panel, name="employee_panel"),
    path("employee/scheduled-trades/", views.scheduled_trades, name="scheduled_trades"),
    path("employee/confirm-trades/<int:trade_id>/<int:employee_id>", views.confirm_trade, name="confirm_trade"),
    path("employee/expire-trades/<int:trade_id>/<int:employee_id>", views.expire_trade, name="expire_trade"),
    path("employee/confirmed-trades/", views.confirmed_trades, name="confirmed_trades"),
]
