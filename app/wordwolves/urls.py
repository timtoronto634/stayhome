from django.urls import path

from . import views

app_name = "WW"
urlpatterns = [
    path("", views.top, name="top"),
    path("create_room/", views.create_room, name="create_room"),
    path("enter_room/", views.enter_room, name="enter_room"),
    path("room/", views.room, name="room"),
    path("room/<str:room_name>/notice", views.name_notice, name="name_notice"),
    path("room/<str:room_name>/", views.entrance, name="entrance"),
    path("room/<str:room_name>/<str:nickname>/set_pass/", views.set_pass, name="set_pass"),
    path("room/<str:room_name>/<str:nickname>/enter_pass/", views.enter_pass, name="enter_pass"),
    path("room/<str:room_name>/<str:nickname>/mypage/", views.mypage, name="mypage"),
    # path("room/<str:room_name>/<str:nickname>/game", views.game, name="game"),
    path("room/<str:room_name>/<str:nickname>/game_res", views.game_res, name="game_res"),
]
# empty line needed
