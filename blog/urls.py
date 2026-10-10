from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:pk>/", views.detalhe_post, name="detalhe"),
]
