from django.shortcuts import render, redirect
from .forms import PlaylistForm

# Create your views here.

def create_playlist(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)  # 先產生 Playlist 物件但不存入資料庫
            playlist.user = request.user # 綁定目前登入的使用者
            playlist.save() # 真正存到資料庫
            form.save_m2m() # 存 ManyToMany 的歌曲
            return redirect("playlist_list") # ------------------------------------
        
    else:
        form = PlaylistForm()

    return render(request, "create_playlist.html", {"form": form})   # ------------------------------------

