from django.urls import path

from analysis import views

app_name = "analysis"

urlpatterns = [
    path("query/", views.MakeQuery.as_view(), name="make-query"),
]
