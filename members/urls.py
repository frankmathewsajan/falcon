from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("members/", views.member_list, name="member_list"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("members/<str:reg_number>/", views.member_detail, name="member_detail"),
]
