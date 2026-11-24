from django.urls import path
from . import views

urlpatterns = [
    path("db-report/", views.db_lab_report, name="db_lab_report"),
]
