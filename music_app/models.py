from django.db import models

# Create your models here.
class Song(models.Model): # Django ORM 的資料表基底
    song = models.TextField()
    singer = models.TextField()
    last_modify_day = models.DateField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music" # 預設表名會是 music_app_song（app 名稱 + model 名稱）from music_app.models import music
