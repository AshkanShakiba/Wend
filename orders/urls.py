from django.urls import path

from .views import home, idle, select, order, about

urlpatterns = [
    path("", home, name="home"),
    path("idle", idle, name="idle"),
    path("select", select, name="select"),
    path("order/<int:product_id>", order, name="order"),
    path("about", about, name="about"),
]
