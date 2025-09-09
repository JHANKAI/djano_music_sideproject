from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.UserRegisterView.as_view(), name="register"), # 註冊
    path("login/", auth_views.LoginView.as_view(), name="login"), # 登入
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("index")), name="logout"), # 登出
    path("playlist/create/", views.CreatePlaylist.as_view(), name="create_playlist"), # 建立音樂清單
    path("playlist/<int:pk>/delete/", views.PlaylistDeleteView.as_view(), name="delete_playlist"),# 刪除音樂清單
    path("playlist/<int:pk>/update/", views.PlaylistUpdateView.as_view(), name="update_playlist"),# 修改音樂清單
    path("playlist/<int:pk>/", views.PlaylistDetailView.as_view(), name="playlist_detail"), # 檢視音樂清單裡的歌曲
    path("playlist/", views.PlaylistView.as_view(), name="playlist_view"), # 檢視音樂清單
    path("song/", views.add_songs, name="add_songs"), # 檢視歌曲清單
]
