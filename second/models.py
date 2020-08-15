from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30) # 30자 문자열
    content = models.TextField() # 제한 없는 문자열
    created_at = models.DateTimeField(auto_now_add=True) # 생성될 때 작성시간 자동 기록
    updated_at = models.DateTimeField(auto_now=True) # 수정시간 기록

    # 숫자 : models.IntegerField