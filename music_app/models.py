from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Song(models.Model): # Django ORM 的資料表基底
    song = models.TextField()
    singer = models.TextField()
    last_modify_day = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Music" # 預設表名會是 music_app_song（app 名稱 + model 名稱）from music_app.models import music
    
    def __str__(self):
        return f"{self.song} - {self.singer}" 



class Playlist(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey (User, on_delete = models.CASCADE)
    songs = models.ManyToManyField(Song, related_name="playlists")  # related_name 是指從被關聯的模型回過頭查詢這個模型時，要用什麼名稱
    created = models.DateTimeField(auto_now_add=True)
    
   
    def __str__(self): 
        return self.name
