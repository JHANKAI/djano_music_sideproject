from django.shortcuts import render, redirect
from .forms import PlaylistForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

# @login_required(login_url='/login/')
def create_playlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PlaylistForm(request.POST)
            if form.is_valid():
                playlist = form.save(commit=False)
                playlist.user = request.user
                playlist.save()
                form.save_m2m()
                return redirect("playlist_list")
        else:
            form = PlaylistForm()
    else:
        form = AuthenticationForm()

    return render(request, "create_playlist.html", {"form": form})   # ------------------------------------



def index(request):
    return render(request, "index.html")

