from django import forms
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'description', 'songs'] # 讓使用者輸入清單名稱、描述、選擇歌曲
        widgets = {
            'songs': forms.CheckboxSelectMultiple, # 多選歌曲
            'name': forms.TextInput(attrs={'placeholder': '請輸入清單名稱'}),
            'description': forms.Textarea(attrs={'placeholder': '選填：輸入清單描述'}),
        }



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)