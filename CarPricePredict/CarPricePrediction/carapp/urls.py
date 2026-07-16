from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict, name="predict"),
    path("result/", views.predict, name="result"),   # Same view ko result ke naam se bhi chalao
]