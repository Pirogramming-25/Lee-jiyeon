from django.http import HttpResponse
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "my_gpt"


def _todo(request):
    return HttpResponse("준비 중")


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="my_gpt:sentiment"), name="home"),

    path("sentiment/", views.sentiment, name="sentiment"),
    path("sentiment/run/", views.sentiment_run, name="sentiment_run"),
    path("summarize/", views.summarize, name="summarize"),
    path("summarize/run/", views.summarize_run, name="summarize_run"),
    path("moderate/", views.moderate, name="moderate"),
    path("moderate/run/", views.moderate_run, name="moderate_run"),

    # 아직 미구현 — 임시로 막아둠
    path("combo/", _todo, name="combo"),
]