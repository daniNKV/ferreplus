from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("allauth.urls")),
    path("employee", views.employee_panel, name="employee_panel"),
    path("employee/scheduled-trades", views.scheduled_trades, name="scheduled_trades"),
    path("employee/confirm-trades/<int:trade_id>", views.confirm_trade, name="confirm_trade"),
    path("employee/expire-trades/<int:trade_id>", views.expire_trade, name="expire_trade"),
    path("employee/confirmed-trades", views.confirmed_trades, name="confirmed_trades"),
    path("employee/show_statistics", views.show_statistics, name="show_statistics"),
    path("employee/historical-states-trades", views.historical_states_trades, name="historical_states_trades"),
    path("employee/weekly-states-trades", views.weekly_states_trades, name="weekly_states_trades"),
    path("employee/category-trades", views.category_trades, name="category_trades"),
    path("employee/users-ages", views.users_ages, name="users_ages"),
    path("employee/sold-products", views.sold_products, name="sold_products"),
]
