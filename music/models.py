from django.db import models


# Create your models here.

class Music(models.Model):
    class Meta:
        db_table = 'music_info'  # 表名

    id = models.AutoField(max_length=11, db_column='music_id', primary_key=True)
    name = models.CharField(max_length=255, db_column='music_name', blank=False)
    singer = models.CharField(max_length=255, db_column='singer', blank=False)
    came_from = models.CharField(max_length=255, db_column='came_from', blank=True)
    kbps = models.CharField(max_length=255, db_column='music_kbps', blank=True)
    size = models.CharField(max_length=255, db_column='music_size', blank=True)
    language = models.CharField(max_length=255, db_column='music_language', blank=True)
    released_data = models.CharField(max_length=255, db_column='released_data', blank=True)
    url = models.CharField(max_length=255, db_column='bdyun_url', blank=False)
    password = models.CharField(max_length=255, db_column='bdyun_password', blank=True)

# class info(models.Model):  # 类名即表名，在生成数据库的时候django会自动将appname和类名拼接起来，即appname_music
#     # class Meta:
#     #     db_table = 'music_info'
#     music_id = models.AutoField(max_length=11, primary_key=True)
#     music_name = models.CharField(max_length=255, blank=False)
#     singer = models.CharField(max_length=255, blank=False)
#     came_from = models.CharField(max_length=255, blank=True)
#     music_kbps = models.CharField(max_length=255, blank=True)
#     music_size = models.CharField(max_length=255, blank=True)
#     music_language = models.CharField(max_length=255, blank=True)
#     released_data = models.CharField(max_length=255, blank=True)
#     bdyun_url = models.CharField(max_length=255, blank=False)
#     bdyun_password = models.CharField(max_length=255, blank=True)
