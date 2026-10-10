from django.urls import path

from . import views

app_name = "chatbot"

urlpatterns = [
    path("", views.chat_page, name="chat"),
    path("api/modelos/", views.api_modelos, name="api_modelos"),
    path("api/enviar/", views.api_enviar, name="api_enviar"),
    path("api/limpar/", views.api_limpar, name="api_limpar"),
]
