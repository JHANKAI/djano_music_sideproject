from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import PlaylistForm,SongListForm
from .models import Playlist, Song
# Create your views here.

def index(request):
    return render(request, "index.html")


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy("index")


class CreatePlaylist(LoginRequiredMixin, CreateView):
    form_class = PlaylistForm
    template_name = "create_playlist.html"
    success_url = reverse_lazy("playlist_view")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PlaylistView(LoginRequiredMixin,ListView): # 看目前使用者所建立的所有音樂清單
    model = Playlist
    template_name = "playlist.html"  # 自訂 template
    context_object_name = 'playlists'      # 在 template 裡用的變數
    
    def get_queryset(self):
        # 只回傳目前登入使用者的 Playlist
        return Playlist.objects.filter(user=self.request.user)

class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = "playlist_detail.html"
    context_object_name = "playlist"


class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = "playlist_delete.html"
    success_url = reverse_lazy("playlist_view")


class PlaylistUpdateView(UpdateView):
    model = Playlist
    template_name = "playlist_update.html"
    form_class = PlaylistForm
    success_url = reverse_lazy("playlist_view")


@login_required
def add_songs(request):
        if request.method == "POST":
            song_form = SongListForm(request.POST)
            playlist_id = request.POST.get('playlist_id')
            new_name = request.POST.get('new_playlist')
            new_desc = request.POST.get('new_description')
            if song_form.is_valid():
                selected_songs = song_form.cleaned_data['songs']
                # 使用者同時選現有音樂清單和輸入新音樂清單名稱 → 錯誤
                if playlist_id and new_name:
                    messages.error(request, "請選擇加入現有音樂清單或創建新的音樂清單，不可同時選擇！")
                    return redirect("add_songs")
                # 選擇現有音樂清單
                if playlist_id and not new_name:
                    playlist = Playlist.objects.get(id=playlist_id, user=request.user)
                    playlist.songs.add(*selected_songs)
                    messages.success(request, "歌曲已成功加入音樂清單！")
                    return redirect("playlist_view")
                # 新增音樂清單
                if new_name and not playlist_id:
                    playlist = Playlist.objects.create(
                        user=request.user,
                        name=new_name,
                        description=new_desc
                    )
                    playlist.songs.add(*selected_songs)
                    messages.success(request, f"已建立新音樂清單「{new_name}」並加入歌曲！")
                    return redirect("playlist_view")
                if not playlist_id and not new_name:
                    messages.error(request, "請選擇一個音樂清單或創建新的音樂清單！")
                    return redirect("add_songs")
            else:
                messages.error(request, "請至少選擇一首歌曲！")
                return redirect("add_songs")
        # GET 方法，顯示表單
        song_form = SongListForm()
        playlists = Playlist.objects.filter(user=request.user)
        return render(request, "songs.html", {"form": song_form, "playlists": playlists})




