from django import forms
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fileds = ['name', 'description', 'songs'] # 讓使用者輸入清單名稱、描述、選擇歌曲
        widgets = {
            'songs': forms.CheckboxSelectMultiple, # 多選歌曲
        }
