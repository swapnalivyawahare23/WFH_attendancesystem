from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("check-in/", views.check_in, name="check_in"),
path("check-out/", views.check_out, name="check_out"),
path("attendance-history/", views.attendance_history, name="attendance_history"),
]