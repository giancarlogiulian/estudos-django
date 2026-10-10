from django.contrib import admin
from django.urls import include, path

from loja.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("blog/", include("blog.urls")),
    path("loja/", include("loja.urls")),
    path("chatbot/", include("chatbot.urls")),
]
