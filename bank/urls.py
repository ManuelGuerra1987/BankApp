
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),
    path("eur_exchange/", views.eur_exchange, name="eur_exchange"),
    path("stocks/", views.stocks, name="stocks"),
    path("history/", views.history, name="history"),

    # API Routes
    path("get_name/<str:receiver_account_number>", views.get_name, name="get_name"),
    path("get_eur_price/", views.get_eur_price, name="get_eur_price"),
    path("get_stock_price/<str:symbol>", views.get_stock_price, name="get_stock_price")

]
