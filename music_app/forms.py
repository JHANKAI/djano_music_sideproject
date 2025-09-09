from django import forms
from .models import Playlist,Song


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'songs'] # 讓使用者輸入清單名稱、描述、選擇歌曲
        widgets = {
            'songs': forms.CheckboxSelectMultiple, # 多選歌曲
            'name': forms.TextInput(attrs={'placeholder': '請輸入清單名稱', 'class': 'input-style'}),
            'description': forms.Textarea(attrs={'placeholder': '選填：輸入清單描述', 'class': 'input-style'}),
        }
        labels = {
            'name': '清單名稱',        # 將 name 改成「清單名稱」
            'description': '清單描述', # 將 description 改成「清單描述」
            'songs': '選擇歌曲',      # 將 songs 改成「選擇歌曲」
        }


class SongListForm(forms.Form):
    songs = forms.ModelMultipleChoiceField(
        label="歌曲清單",
        queryset=Song.objects.all(),  # 把所有歌曲抓出來
        widget=forms.CheckboxSelectMultiple,
        required=True
    )




